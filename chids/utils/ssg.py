import networkx as nx
from collections import Counter
from chids.utils.process_args import get_filepath
from chids.conf.config import SYSCALLS_ARGS
from chids.shared.constants import *


class SSGraph:

    def __init__(self, sequence_data, seen_syscalls, seen_args):
        self.sequence_data = sequence_data
        self.seen_syscalls = seen_syscalls
        self.seen_args = seen_args
        self.ssg_edges = []

    def _get_graph(self, g_edges):
        graph = nx.DiGraph((x, y, {WEIGHT: v}) for (x, y), v in Counter(g_edges).items())
        return graph

    def _get_graph_size(self, graph):
        return graph.size(weight=WEIGHT)

    def _get_usi(self, distinct_unseen_syscalls, sequence_graph):

        if distinct_unseen_syscalls:
            usn_in_centrality = nx.in_degree_centrality(sequence_graph).get(USN)
            usn_out_centrality = nx.out_degree_centrality(sequence_graph).get(USN)

            if isinstance(usn_in_centrality, type(None)):
                usn_in_centrality = 0

            if isinstance(usn_out_centrality, type(None)):
                usn_out_centrality = 0

            return len(distinct_unseen_syscalls) * (usn_in_centrality + usn_out_centrality)

        else:
            return 0

    def _get_uai(self, distinct_unseen_args, distinct_syscalls_with_args, sequence_graph):

        if distinct_unseen_args:
            uan_in_centrality = nx.in_degree_centrality(sequence_graph).get(UAN)
            uan_out_centrality = nx.out_degree_centrality(sequence_graph).get(UAN)

            if isinstance(uan_in_centrality, type(None)):
                uan_in_centrality = 0

            if isinstance(uan_out_centrality, type(None)):
                uan_out_centrality = 0

            return len(distinct_syscalls_with_args) * len(distinct_unseen_args) * (uan_in_centrality + uan_out_centrality)

        else:
            return 0

    def get_ssg_features(self):

        # get distinct unseen syscalls
        distinct_unseen_syscalls = set(self.sequence_data.loc[~self.sequence_data.syscall.isin(self.seen_syscalls)][SYSCALL_COL].tolist())

        # aggregate all unseen syscalls under the USN node
        self.sequence_data.loc[~self.sequence_data.syscall.isin(self.seen_syscalls), SYSCALL_COL] = USN

        # process the arguments of open, stat, execve, and clone syscalls
        self.sequence_data.loc[self.sequence_data.syscall.isin([USN]), ARGS_COL] = EMPTY
        self.sequence_data.loc[self.sequence_data.syscall.isin([STAT, OPEN]), ARGS_COL] = \
            self.sequence_data[ARGS_COL].str[1].dropna().apply(get_filepath, args=(MODE_SO,))
        self.sequence_data.loc[self.sequence_data.syscall.isin([EXECVE]), ARGS_COL] = \
            self.sequence_data[ARGS_COL].str[0].dropna().apply(get_filepath, args=(MODE_EX,))
        self.sequence_data.loc[self.sequence_data.syscall.isin([CLONE]), ARGS_COL] = \
            self.sequence_data[ARGS_COL].str[1].dropna().apply(get_filepath, args=(MODE_CL,))

        # get distinct syscalls (open, stat, clone, execve) that involve unseen args
        distinct_syscalls_with_unseen_args = set(
            self.sequence_data.loc[(self.sequence_data.syscall.isin(SYSCALLS_ARGS)) & self.sequence_data.args.notnull()
                    & (~self.sequence_data.args.isin(self.seen_args))][SYSCALL_COL].tolist())

        # aggregate all unseen arguments under the UAN node
        self.sequence_data.loc[(self.sequence_data.syscall.isin(SYSCALLS_ARGS)) & self.sequence_data.args.notnull() &
            (~self.sequence_data.args.isin(self.seen_args)), SYSCALL_COL] = UAN

        # get distinct unseen arguments
        distinct_unseen_args = set(self.sequence_data.loc[(self.sequence_data.syscall.isin([UAN]))][ARGS_COL].tolist())

        # prepare the SSG edges
        syscalls_list = self.sequence_data[SYSCALL_COL].tolist()
        for i in range(len(syscalls_list) - 1):
            self.ssg_edges.append((syscalls_list[i], syscalls_list[i + 1]))


        ssg = self._get_graph(self.ssg_edges)

        # get the SSG features
        usi = self._get_usi(distinct_unseen_syscalls, ssg)
        uai = self._get_uai(distinct_unseen_args, distinct_syscalls_with_unseen_args, ssg)
        ssg_size = self._get_graph_size(ssg)


        return usi, uai, ssg_size