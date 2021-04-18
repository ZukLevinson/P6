import tensorflow as tf
import numpy as np

from wiki_reader import WikiReader
from csv_writer import CSVWriter

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Embedding
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

LSTM = tf.compat.v1.keras.layers.CuDNNLSTM


class WordPredictor(Sequential):
    def __init__(self, num_of_words, **kwargs):
        super(WordPredictor, self).__init__()

        self.NUMBER_OF_WORDS = num_of_words
        self.VOCABULARY_SIZE = 6000

        self.tokenizer = Tokenizer()

        # NETWORK
        self.add(Embedding(input_dim=self.VOCABULARY_SIZE, output_dim=50, input_length=self.NUMBER_OF_WORDS))
        self.add(LSTM(256, return_sequences=True))
        self.add(Dropout(0.2))
        self.add(LSTM(256))
        self.add(Dropout(0.2))
        self.add(Dense(self.VOCABULARY_SIZE, activation='softmax'))

    # def train_on_wiki(self):
    #     self.fit(create_pre_process_generator(wiki_set_generator, self.tokenizer, self.VOCABULARY_SIZE), epochs=100,
    #              steps_per_epoch=256)


def create_pre_process_generator(wiki_sets, tokenizer, vocab_size):
    for wiki_set in wiki_sets:
        tokenizer.fit_on_texts([wiki_set])
        sequence = np.array(tokenizer.texts_to_sequences([wiki_set]))

        x, y = sequence[:, :-1], sequence[:, -1]
        y = to_categorical(y, vocab_size)

        yield x, y


def predict_words(tf_model, tokenizer, text_seq_length, seed_text, n_words):
    text = []

    for _ in range(n_words):
        encoded = tokenizer.texts_to_sequences([seed_text])[0]
        encoded = pad_sequences([encoded], maxlen=text_seq_length, truncating='pre')

        y_predict = np.argmax(tf_model.predict(encoded), axis=-1)

        predicted_word = ''
        for word, index in tokenizer.word_index.items():
            if index == y_predict:
                predicted_word = word
                break
        seed_text = seed_text + ' ' + predicted_word
        text.append(predicted_word)
    return ' '.join(text)


def get_lines_separated(tokens, sentence_length=20):
    for index in range(sentence_length, len(tokens)):
        sequence = tokens[index - sentence_length:index]

        sentence = ' '.join(sequence[:sentence_length - 1])
        target = sequence[sentence_length - 1]

        yield [sentence, target]


def generate_sets(set_length=20, max_rows=10000, max_folders=1000):
    writer = CSVWriter()

    folder_name = writer.create_folder()
    csv_name = writer.create_csv_file(folder_name)

    reader = WikiReader(min_words_per_page=300)

    file_name = f"{folder_name}/{csv_name}.csv"

    for page_tokens in reader.get_and_reformat_pages(set_length):
        if writer.count_rows(file_name) > max_rows:
            if writer.count_csv_in_folder(folder_name) > max_folders:
                folder_name = writer.create_folder()

            csv_name = writer.create_csv_file(folder_name)

            file_name = f"{folder_name}/{csv_name}.csv"

        writer.add_rows(file_name, [row for row in get_lines_separated(page_tokens)])


if __name__ == "__main__":
    generate_sets(300)
