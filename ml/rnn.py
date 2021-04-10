import tensorflow as tf
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Embedding
from tensorflow.keras.utils import to_categorical
LSTM = tf.compat.v1.keras.layers.CuDNNLSTM

