import tensorflow as tf
import numpy as np

from reader import WikiReader

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Embedding
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.text import Tokenizer

LSTM = tf.compat.v1.keras.layers.CuDNNLSTM


def pre_process_lines(lines):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(lines)
    return np.array(tokenizer.texts_to_sequences(lines)), len(tokenizer.word_index) + 1


if __name__ == "__main__":
    reader = WikiReader(100, pages=5)
    reader.get_and_reformat_all_pages()
    reader.generate_sentences(20)

    sequences, VOCABULARY_SIZE = pre_process_lines(reader.generate_sentences(20))
    x, y = sequences[:, :-1], sequences[:, -1]

    SEQUENCE_LENGTH = x.shape[1]
    y = to_categorical(y, num_classes=VOCABULARY_SIZE)

    model = Sequential()
    model.add(Embedding(input_dim=VOCABULARY_SIZE, output_dim=20, input_length=SEQUENCE_LENGTH))
    model.add(LSTM(100, return_sequences=True))
    model.add(LSTM(100))
    model.add(Dense(100, activation='relu'))
    model.add(Dense(VOCABULARY_SIZE, activation='softmax'))
    model.summary()

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(x, y, batch_size=256, epochs=100)
    model.save('shakespeare-RNN')
