# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Activation, BatchNormalization, Dense, Dropout, Flatten, Softmax

# ----------------------------------------------------------------------------------------------------------------------
# Define Multi-Layer Perceptron
# ----------------------------------------------------------------------------------------------------------------------


def MLP():
    """
    Multi-Layer Perceptron for the classification of Asteroid Taxonomy and Family.

    Structure
    ---------
    Input
    """
    model = Sequential()

    model.add(Flatten(input_shape=()))
    model.add(Dense())
    model.add(Activation('relu'))

    model.add(Dense(2))
    model.add(Activation('softmax'))

    return model
