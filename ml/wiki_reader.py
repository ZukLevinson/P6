import random
import string
import wikipedia
import re
from requests.exceptions import ConnectionError, HTTPError
from time import sleep


def get_random_wiki_pages(number_of_pages, minimum_words_count):
    titles = wikipedia.random(number_of_pages)

    if not isinstance(titles, list):
        titles = [titles]

    for title in titles:
        page = get_page_contents(title)

        while len(get_page_contents(title).split()) < minimum_words_count:
            title = wikipedia.random()

        yield title, page


def get_page_contents(title):
    try:
        return wikipedia.page(title, auto_suggest=True).content
    except wikipedia.DisambiguationError as e:
        return get_page_contents(random.choice(e.options))
    except (wikipedia.PageError, ConnectionError, RecursionError):
        return get_page_contents(wikipedia.random())
    except HTTPError:
        sleep(2)
        return get_page_contents(wikipedia.random())
    finally:
        print(f"Added page named '{title}'")


class WikiReader:
    def __init__(self, min_words_per_page, **kwargs):
        self.MINIMUM_WORD_COUNT = min_words_per_page

        self.page_names = []

    def get_and_reformat_pages(self, number_of_pages=3):
        for title, page in get_random_wiki_pages(number_of_pages, self.MINIMUM_WORD_COUNT):
            self.page_names.append(title)  # TODO: add title check to disable page duplication
            yield format_content(page)


def format_content(text):
    text = re.sub("[\(\[].*?[\)\]]", "", text)  # remove text inside parenthesis

    doc_tokens = text.split()
    translate_punctuation_table = str.maketrans('', '', string.punctuation)
    doc_tokens = [w.translate(translate_punctuation_table) for w in doc_tokens]  # edit text according to table
    doc_tokens = [word for word in doc_tokens if word.isalnum()]  # check if all words are alphanumeric
    doc_tokens = [word.lower() for word in doc_tokens]  # lowercase text

    return doc_tokens
