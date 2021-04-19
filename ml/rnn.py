import tensorflow as tf
import numpy as np
import time

from wiki_reader import WikiReader, format_content
from csv_writer import CSVWriter
from file_reader import FileReader

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Embedding
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

LSTM = tf.compat.v1.keras.layers.CuDNNLSTM


class WordPredictor(Sequential):
    def __init__(self, num_of_words, **kwargs):
        super(WordPredictor, self).__init__()

        reader = FileReader()

        self.NUMBER_OF_WORDS = num_of_words

        self.tokenizer = Tokenizer()

        self.VOCABULARY_SIZE = reader.vocabulary(self.tokenizer)


        # NETWORK
        # self.add(Embedding(input_dim=self.VOCABULARY_SIZE, output_dim=50, input_length=self.NUMBER_OF_WORDS))
        # self.add(LSTM(256, return_sequences=True))
        # self.add(Dropout(0.2))
        # self.add(LSTM(256))
        # self.add(Dropout(0.2))
        # self.add(Dense(self.VOCABULARY_SIZE, activation='softmax'))
        self.add(Embedding(input_dim=self.VOCABULARY_SIZE, output_dim=50, input_length=self.NUMBER_OF_WORDS))
        self.add(LSTM(100, return_sequences=True))
        self.add(LSTM(100))
        self.add(Dense(100, activation='relu'))
        self.add(Dense(self.VOCABULARY_SIZE, activation='softmax'))

        self.compile(loss='categorical_crossentropy', optimizer='adam',
                     metrics=['accuracy', tf.keras.metrics.MeanAbsoluteError()])

    def train_on_wiki(self, epochs=100, steps_per_epoch=10):
        self.fit(create_pre_process_generator(epochs * steps_per_epoch, self.tokenizer, self.VOCABULARY_SIZE,
                                              line_count=1),
                 epochs=epochs,
                 steps_per_epoch=steps_per_epoch)
        self.save_weights(f"weights/rnn-{time.time()}")

    def load_model(self):
        self.load_weights("weights/rnn-1618827756.9249594")

    def predict_words(self, text_seq_length, seed_text, n_words):
        text = []

        for _ in range(n_words):
            encoded = self.tokenizer.texts_to_sequences([seed_text])[0]
            encoded = pad_sequences([encoded], maxlen=text_seq_length, truncating='pre')

            y_predict = np.argmax(self.predict(encoded), axis=-1)

            predicted_word = ''
            for word, index in self.tokenizer.word_index.items():
                if index == y_predict:
                    predicted_word = word
                    break
            seed_text = seed_text + ' ' + predicted_word
            text.append(predicted_word)
        return ' '.join(text)


def create_pre_process_generator(num_of_sets, tokenizer, vocab_size, line_count=1):
    reader = FileReader()

    for i in range(num_of_sets):
        wiki_set = [' '.join(line) for line in reader.get_lines(line_count)]
        sequence = np.array([token_list for token_list in tokenizer.texts_to_sequences(wiki_set)])

        x, y = np.asarray([line[:-1] for line in sequence], dtype=np.int32), [line[-1] for line in sequence]
        y = to_categorical(y, num_classes=vocab_size)

        yield x, y


def get_lines_separated(tokens, sentence_length=50):
    for index in range(sentence_length, len(tokens)):
        sequence = tokens[index - sentence_length:index]

        sentence = ' '.join(sequence[:sentence_length - 1])
        target = sequence[sentence_length - 1]

        yield [sentence, target]


def generate_sets(set_length=200, max_rows=200000, max_folders=1000):
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
    rnn = WordPredictor(49)

    # Train RNN
    rnn.train_on_wiki(100, 256)

    # Generate new sets
    # generate_sets(200000)

    # Load weights
    # rnn.load_model()

    # Predict
    # print(rnn.predict_words(1, "hello", 10))
