import os
import numpy as np
import pandas as pd
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from keras.layers import Input, Dense
from keras.models import Model
from keras import regularizers
from chids.shared.misc import _format_input
from chids.conf.config import *
from chids.shared.constants import *


class Training:

    def __init__(self, anomaly_vectors):
        self.anomaly_vectors = anomaly_vectors


    def _autoencoder_model(self, vectors):
        inputs = Input(shape=(vectors.shape[1], vectors.shape[2]))

        # encoder
        L1 = Dense(ENCODING_DIM, activation=ACTIVATION, activity_regularizer=regularizers.l1(REG_RATE))(inputs)
        L2 = Dense(BOTTLENECK, activation=ACTIVATION)(L1)

        #decoder
        L3 = Dense(BOTTLENECK, activation=ACTIVATION)(L2)
        L4 = Dense(DECODING_DIM, activation=ACTIVATION)(L3)

        output = Dense(vectors.shape[2], activation=ACTIVATION)(L4)
        model = Model(inputs=inputs, outputs=output)
        return model

    def _get_thresholds_list(self, model, inp):
        thresh_list = []
        prediction = model.predict(inp, verbose=VERBOSE)
        prediction = prediction.reshape(prediction.shape[0], prediction.shape[2])
        inp = inp.reshape(inp.shape[0], inp.shape[2])
        training_reconstruction_errors = np.mean(np.square(prediction - inp), axis=1)

        for _theta in np.arange(0.2, 2.2, 0.2):
            thresh_list.append(max(training_reconstruction_errors) * _theta)
        return thresh_list

    def train_model(self):
        formatted_anomaly_vectors = _format_input(self.anomaly_vectors)
        training_anomaly_vectors = formatted_anomaly_vectors.reshape(formatted_anomaly_vectors.shape[0], 1, formatted_anomaly_vectors.shape[1])
        model = self._autoencoder_model(training_anomaly_vectors)
        model.compile(optimizer=OPTIMIZER, loss=LOSS_FUNC)
        model.fit(training_anomaly_vectors, training_anomaly_vectors, epochs=EPOCH, batch_size=BATCH_SIZE, validation_split=VALIDATION_SPLIT, verbose=VERBOSE)
        thresh_list = self._get_thresholds_list(model, training_anomaly_vectors)
        return thresh_list, model











