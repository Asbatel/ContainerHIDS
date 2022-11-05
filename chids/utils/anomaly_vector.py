import multiprocessing

from chids.conf.config import BETA_FOLD_INCREASE, CHUNK_SIZE
from chids.utils.ssg import SSGraph
from multiprocessing import Pool

class AnomalyVector:

    def __init__(self, traces, seen_syscalls, seen_args, max_freq_syscalls):
        self.traces = traces
        self.seen_syscalls = seen_syscalls
        self.seen_args = seen_args
        self.max_s = max_freq_syscalls


    def construct_anomaly_vector(self, trace):
        anomaly_vectors = []
        for sequence in trace:

            if sequence.empty:
                anomaly_vectors.append([])

            else:
                graph_ob = SSGraph(sequence, self.seen_syscalls, self.seen_args)
                usi, uai, ssg_size = graph_ob.get_ssg_features()
                fi = ssg_size / (self.max_s * BETA_FOLD_INCREASE)
                anomaly_vector = [fi, usi, uai]
                anomaly_vectors.append(anomaly_vector)



        return anomaly_vectors


    def get_anomaly_vectors(self):
        pool = Pool()
        all_anomaly_vectors = pool.map(self.construct_anomaly_vector, self.traces, chunksize=CHUNK_SIZE)

        return all_anomaly_vectors

