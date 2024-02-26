""" Implement the GraphNode and its sub-classes. Sub-classes graphlib._NodeInfo.

For use with Graph- and Tree-like problem state spaces searches.
"""
import numpy as np

from typing import override

from ..core.logger import logger


__all__ = ["Neuron"]


class Neuron(object):
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
        self.weights = weights
        self.error = 2.

    def score(self, x, y) -> float:
        return 1 / (1 + np.exp(self.weights[0] * x + self.weights[1] * y + self.weights[2]))

    @override
    def __repr__(self) -> str:
        return f'Neuron#{hash(self)}:{self.weights}. err={self.error}'
 
    @override
    def __hash__(self) -> int:
        return hash(self.weights)

    @override
    def __eq__(self, other) -> bool:
        return self.weights == other.weights
