""" Implement the ProblemGraph class. Sub-classes graphlib.TopologicalSorter.

For use with Graph- and Tree-like problem state spaces searches.
"""
from graphlib import TopologicalSorter
from typing import Set

from ..core.logger import logger
from .node import GraphNode


__all__ = ["ProblemGraph"]


class ProblemGraph(TopologicalSorter):

    def __init__(self, graph:dict[GraphNode, Set[GraphNode]]) -> None:
        """Initialize an instance of ProblemGraph.

        :param graph: dict of Node -> set of Successors
        :type graph: dict[GraphNode, Set[GraphNode]]
        :raises TypeError: If graph is None
        """
        logger.debug("initializing %s", self.__class__.__name__)
        if graph is None:
            raise TypeError("graph : dict[GraphNode, Set[GraphNode]] : Cannot be None")
        super().__init__(graph)
        logger.debug("graph %s", self)

    def __repr__(self) -> str:
        return f'ProblemGraph: {[n for n in self._node2info]}'
