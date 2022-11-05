import itertools
import multiprocessing

from chids.conf.config import CHUNK_SIZE
from chids.shared.constants import *
from multiprocessing import Pool

class SeenSyscalls:

    def __init__(self, scaps_dfs):
        self.scaps_dfs = scaps_dfs

    def _syscalls_per_scap(self, scap_df):
        return set(list(scap_df[SYSCALL_COL]))

    def seen_syscalls(self):
        pool = Pool()
        all_syscalls = pool.map(self._syscalls_per_scap, self.scaps_dfs, chunksize=CHUNK_SIZE)
        seen_syscalls = set(list(itertools.chain.from_iterable(all_syscalls)))
        return list(seen_syscalls)
