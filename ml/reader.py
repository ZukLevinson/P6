import random
import string
import wikipedia
import re


def get_random_wiki_pages(number_of_pages, minimum_words_count):
    titles = wikipedia.random(number_of_pages)

    if number_of_pages > 1:
        for title in titles:
            page = get_page_contents(title)

            while len(page.split()) < minimum_words_count:
                page = get_page_contents(wikipedia.random())

            yield page
    else:
        page = get_page_contents(titles)

        while len(page.split()) < minimum_words_count:
            page = get_page_contents(wikipedia.random())

        yield page


def get_page_contents(title):
    try:
        return wikipedia.page(title).content
    except wikipedia.DisambiguationError as e:
        new_title = random.choice(e.options)

        return wikipedia.page(new_title).content


class WikiReader:
    def __init__(self, min_words, **kwargs):
        self.NUMBER_OF_PAGES = 1 if kwargs.get('pages') is None else kwargs.get('pages')
        self.MINIMUM_WORD_COUNT = min_words

        self.pages = []

    def get_and_reformat_all_pages(self):
        for page in get_random_wiki_pages(self.NUMBER_OF_PAGES, self.MINIMUM_WORD_COUNT):
            self.pages.append(format_content(page))

    def generate_sentences(self, num_of_words):
        sentences = []

        for page_tokens in self.pages:
            for i in range(num_of_words, len(page_tokens)):
                sequence = page_tokens[i - num_of_words:i]
                line = ' '.join(sequence)
                sentences.append(line)

        return sentences


def format_content(text):
    text = re.sub("[\(\[].*?[\)\]]", "", text)  # remove text inside parenthesis

    doc_tokens = text.split()
    translate_punctuation_table = str.maketrans('', '', string.punctuation)
    doc_tokens = [w.translate(translate_punctuation_table) for w in doc_tokens]  # edit text according to table
    doc_tokens = [word for word in doc_tokens if word.isalnum()]  # check if all words are alphanumeric
    doc_tokens = [word.lower() for word in doc_tokens]  # lowercase text

    return doc_tokens
