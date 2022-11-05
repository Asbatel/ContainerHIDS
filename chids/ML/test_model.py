from multiprocessing import Pool
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import numpy as np
import pandas as pd
from chids.shared.constants import *
from chids.shared.misc import _format_input
from keras.models import load_model

class Testing:

    def __init__(self, trained_model, thresh_list):
        self.trained_model = trained_model
        self.thresh_list = thresh_list

    def _get_reconstruction_loss(self, scap_anomaly_vectors):
        formatted_anomaly_vectors = _format_input(scap_anomaly_vectors, TRAINING_MODE=False)
        trace_anomaly_vectors = formatted_anomaly_vectors.reshape(formatted_anomaly_vectors.shape[0], 1, formatted_anomaly_vectors.shape[1])
        modell = load_model(self.trained_model)
        trace_prediction = modell.predict(trace_anomaly_vectors, verbose=1)
        trace_prediction = trace_prediction.reshape(trace_prediction.shape[0], trace_prediction.shape[2])
        trace_anomaly_vectors = trace_anomaly_vectors.reshape(trace_anomaly_vectors.shape[0], trace_anomaly_vectors.shape[2])
        errors = np.mean(np.square(trace_prediction - trace_anomaly_vectors), axis=1)
        return errors


    def _classify(self, scap_anomaly_vectors):

        result = pd.DataFrame()
        result[LOSS] = self._get_reconstruction_loss(scap_anomaly_vectors)
        result_of_thetas = []

        for threshold in self.thresh_list:

            result[ANOMALY] = result[LOSS] > threshold
            result[NORMAL] = result[LOSS] <= threshold

            is_anomalous = True if len(result[result[ANOMALY] == True]) > 0 else False

            result_of_thetas.append(is_anomalous)


        return result_of_thetas

    def get_classifications(self, scap_anomaly_vectors):

        pool = Pool()
        all_results = pool.map(self._classify, scap_anomaly_vectors)

        return all_results


