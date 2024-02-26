""" Implement the GraphNode and its sub-classes. Sub-classes graphlib._NodeInfo.

For use with Graph- and Tree-like problem state spaces searches.
"""
from graphlib import _NodeInfo
from typing import Any, override

from ..core.logger import logger


__all__ = ["GraphNode", "Neuron"]


class GraphNode(_NodeInfo):
    
    def __init__(self, node:Any) -> None:
        """Initialize an instance of ProblemGraph.
        
        :param node: The node to represent.
        :type node: Any
        """
        logger.debug("initializing %s", self.__class__.__name__)
        super().__init__(node)

    def __repr__(self) -> str:
        return f'\nGraphNode: {self.node} => [{[s for s in self.successors]}]'

    def __hash__(self) -> int:
        return hash(self.node)


class Neuron(GraphNode):
    DIM_W = 3

    def __init__(self, *weights:tuple[float]) -> None:
        """Initialize an instance of Neuron.

        :param weights: Tuple of weight values.
        :type weights: tuple[float]
        :raises TypeError: If weights is not of length .node.Neuron.DIM_W.
        """
        logger.debug("initializing %s", self.__class__.__name__)
        if weights is None or len(weights) != self.DIM_W:
            raise TypeError(f'weights : tuple[float] : Must be of length {self.DIM_W}.')
        super().__init__(weights)
        self.output : float = None

    @property
    def weights(self) -> tuple[float]:
        return self.node

    @override
    def __repr__(self) -> str:
        return f'{super().__repr__()}\n\tNeuron:{self.weights} = {self.output}'
 
    @override
    def __hash__(self) -> int:
        return hash(self.weights)

    @override
    def __eq__(self, other) -> bool:
        return self.weights == other.weights
