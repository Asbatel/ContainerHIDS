import multiprocessing
import pandas as pd
from chids.conf.config import SYSCALLS_ARGS, SEQUENCE_DURATION, CHUNK_SIZE

pd.options.mode.chained_assignment = None
from chids.shared.constants import *
from multiprocessing import Pool


class Trace:

    def __init__(self, scaps_dfs):
        self.scaps_dfs = scaps_dfs


    def _chunk_scap(self, scap_df):
        trace = []
        timestamps = pd.to_datetime(scap_df['timestamp'])

        if not pd.isnull(timestamps[len(timestamps) - 1]):
            end = timestamps[len(timestamps) -1]
        else:
            end = timestamps[len(timestamps) - 2]

        intervals = pd.date_range(start=timestamps[0], end=end, freq=SEQUENCE_DURATION)


        for i in range(len(intervals)):

            if i == len(intervals) - 1:
                interval_mask = intervals[i] <= timestamps
            else:
                interval_mask = (intervals[i] <= timestamps) & (intervals[i + 1] > timestamps)

            sequence = scap_df[[SYSCALL_COL, ARGS_COL]].loc[interval_mask]
            sequence.loc[~sequence.syscall.isin(SYSCALLS_ARGS), ARGS_COL] = EMPTY

            trace.append(sequence[[SYSCALL_COL, ARGS_COL]])

        return trace


    def trace(self):
        pool = Pool()
        traces = pool.map(self._chunk_scap, self.scaps_dfs, chunksize=CHUNK_SIZE)

        return traces