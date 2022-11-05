import multiprocessing
import pandas as pd
import itertools
from chids.helpers.sysdig import Sysdig
from chids.shared.exceptions import NoSyscallsFound
pd.options.mode.chained_assignment = None
from chids.conf.config import SYSCALLS_ARGS, CHUNK_SIZE
from chids.utils.process_args import get_filepath
from chids.shared.constants import *
from multiprocessing import Pool

class SeenArgs:

    def __init__(self, scaps_dfs):
        self.scaps_dfs = scaps_dfs

    def _get_args(self, scap_df):

        syscalls_with_args = scap_df[[SYSCALL_COL, ARGS_COL]]
        syscalls_with_args.loc[~syscalls_with_args.syscall.isin(SYSCALLS_ARGS), ARGS_COL] = EMPTY

        syscalls_with_args.loc[syscalls_with_args.syscall.isin([STAT, OPEN]), ARGS_COL] = \
            syscalls_with_args[ARGS_COL].str[1].dropna().apply(get_filepath, args=(MODE_SO,))

        syscalls_with_args.loc[syscalls_with_args.syscall.isin([CLONE]), ARGS_COL] = \
            syscalls_with_args[ARGS_COL].str[1].dropna().apply(get_filepath, args=(MODE_CL,))

        syscalls_with_args.loc[syscalls_with_args.syscall.isin([EXECVE]), ARGS_COL] = \
            syscalls_with_args[ARGS_COL].str[0].dropna().apply(get_filepath, args=(MODE_EX,))

        list_of_args = syscalls_with_args.loc[syscalls_with_args.syscall.isin(SYSCALLS_ARGS)
                        & syscalls_with_args.args.notnull()][ARGS_COL].tolist()

        return set(list_of_args)

    def seen_args(self):

        pool = Pool()
        all_args = pool.map(self._get_args, self.scaps_dfs, chunksize=CHUNK_SIZE)

        seen_args = set(list(itertools.chain.from_iterable(all_args)))
        return list(seen_args)




