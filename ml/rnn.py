import tensorflow as tf
import numpy as np

from reader import WikiReader

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Embedding
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

LSTM = tf.compat.v1.keras.layers.CuDNNLSTM


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
    reader = WikiReader(100, pages=200)
    reader.get_and_reformat_all_pages()
    generated_lines = reader.generate_sentences(20)

    sequences, seq_tokenizer = pre_process_lines(generated_lines)

    VOCABULARY_SIZE = len(seq_tokenizer.word_index) + 1
    x, y = sequences[:, :-1], sequences[:, -1]

    SEQUENCE_LENGTH = x.shape[1]
    y = to_categorical(y, num_classes=VOCABULARY_SIZE)

    model = Sequential()

    model.add(Embedding(input_dim=VOCABULARY_SIZE, output_dim=50, input_length=SEQUENCE_LENGTH))
    model.add(LSTM(256, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(256))
    model.add(Dropout(0.2))
    model.add(Dense(y.shape[1], activation='softmax'))

    # model.add(Embedding(input_dim=VOCABULARY_SIZE, output_dim=20, input_length=SEQUENCE_LENGTH))
    # model.add(LSTM(100, return_sequences=True))
    # model.add(LSTM(100))
    # model.add(Dense(100, activation='relu'))
    # model.add(Dense(VOCABULARY_SIZE, activation='softmax'))

    model.summary()

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(x, y, epochs=100, batch_size=256)
    model.save_weights('my_model_weights.h5')  # to store

    basis_text = "hammer is a tool"
    print(basis_text)
    print('\n')
    print(predict_words(model, seq_tokenizer, 20, basis_text, 10))
