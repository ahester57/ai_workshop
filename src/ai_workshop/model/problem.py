""" Implement the ProblemGraph class. Sub-classes graphlib.TopologicalSorter.

For use with Graph- and Tree-like problem state spaces searches.
"""
import networkx as nx
import numpy as np

from graphlib import TopologicalSorter
from typing import Callable, override

from ..core.logger import logger
from .node import Neuron


__all__ = ['ProblemGraph']


class ProblemGraph(TopologicalSorter):

    def __init__(self, initial:Neuron) -> None:
        """Initialize an instance of ProblemGraph.

        :param initial: Neuron
        :type initial: Neuron
        :param evaluate: The evaluation function
        :type evaluate: Callable
        :raises TypeError: If initial is None
        """
        logger.debug('initializing %s', self.__class__.__name__)
        if initial is None:
            raise TypeError('initial : Neuron - Cannot be None')
        super().__init__({initial: {}})
        self.initial : Neuron = self._node2info[initial].node
        self.finished_graph = None
        self.diGraph = nx.DiGraph()

    @override
    def add(self, node, *predecessors) -> None:
        super().add(node, predecessors)
        [self.diGraph.add_edge(pred, node) for pred in predecessors]

    def evaluate_node(self, node:Neuron) -> float:
        """Initialize a Neuron as a potential NAND gate.

        :param initial: Neuron
        :type initial: Neuron
        :return: Sum of errors for each combination
        :rtype: float
        """
        node.error = np.sum([
            np.abs(1 - node.score(0, 0)),
            np.abs(1 - node.score(0, 1)),
            np.abs(1 - node.score(1, 0)),
            np.abs(0 - node.score(1, 1))
        ])
        return node.error

    @property
    def graph(self) -> dict[Neuron, list[Neuron]]:
        if self.finished_graph is None:
            self.finished_graph = dict([(self._node2info[n].node, self._node2info[n].successors) for n in self._node2info])
        return self.finished_graph

    def __repr__(self) -> str:
        return f'ProblemGraph: {self.graph}'
