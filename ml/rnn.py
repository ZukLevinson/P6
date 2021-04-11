import tensorflow as tf
import numpy as np

from reader import WikiReader

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
        self.VOCABULARY_SIZE = 10 ** 5

        self.tokenizer = Tokenizer()

        self.embedding = Embedding(input_dim=self.VOCABULARY_SIZE, output_dim=50, input_length=self.NUMBER_OF_WORDS)
        self.lstm_1 = LSTM(256, return_sequences=True)
        self.drop_1 = Dropout(0.2)
        self.lstm_2 = LSTM(256)
        self.drop_2 = Dropout(0.2)
        self.classifier = Dense(self.VOCABULARY_SIZE, activation='softmax')

    def call(self, inputs, **kwargs):
        # VOCABULARY_SIZE = len(self.tokenizer.word_index) + 1

        current_result = self.embedding(inputs)
        current_result = self.lstm_1(current_result)
        current_result = self.drop_1(current_result)
        current_result = self.lstm_2(current_result)
        current_result = self.drop_2(current_result)
        return self.classifier(current_result)

    def train_on_wiki(self, min_words_in_set=100, num_of_sets=300):
        wiki_reader = WikiReader(min_words_in_set, pages=num_of_sets)
        wiki_set_generator = wiki_reader.create_page_generator(self.NUMBER_OF_WORDS, 20)

        self.fit(create_pre_process_generator(wiki_set_generator, self.tokenizer, self.VOCABULARY_SIZE), epochs=100,
                 steps_per_epoch=256)


def create_pre_process_generator(generator, tokenizer, vocab_size):
    for set in generator:
        tokenizer.fit_on_texts([set])
        sequence = np.array(tokenizer.texts_to_sequences([set]))

        x, y = sequence[:, :-1], sequence[:, -1]
        y = to_categorical(y, vocab_size)

        yield x, y


def pre_process_lines(lines):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(lines)
    return np.array(tokenizer.texts_to_sequences(lines)), tokenizer


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


if __name__ == "__main__":
    model = WordPredictor(200)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.train_on_wiki()

# if __name__ == "__main__":
#     reader = WikiReader(100, pages=10)
#     reader.get_and_reformat_all_pages()
#     generated_lines = reader.generate_sentences(20)
#
#     sequences, seq_tokenizer = pre_process_lines(generated_lines)
#
#     VOCABULARY_SIZE = len(seq_tokenizer.word_index) + 1
#     x, y = sequences[:, :-1], sequences[:, -1]
#
#     # print(x.shape, y.shape)
#
#     SEQUENCE_LENGTH = x.shape[1]
#     y = to_categorical(y, num_classes=VOCABULARY_SIZE)
#
#     model = Sequential()
#
#     print(x.shape)
#     print(x)
#     print(y.shape)
#     print(y)
#
#     model.add(Embedding(input_dim=VOCABULARY_SIZE, output_dim=50, input_length=SEQUENCE_LENGTH))
#     model.add(LSTM(256, return_sequences=True))
#     model.add(Dropout(0.2))
#     model.add(LSTM(256))
#     model.add(Dropout(0.2))
#     model.add(Dense(VOCABULARY_SIZE, activation='softmax'))
#
#     model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
#     model.fit(x, y, epochs=100, batch_size=256)
#     model.save_weights('my_model_weights.h5')  # to store
#
#     basis_text = "hammer is a tool"
#     print(basis_text)
#     print('\n')
#     print(predict_words(model, seq_tokenizer, 20, basis_text, 10))
