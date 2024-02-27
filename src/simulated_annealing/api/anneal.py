""" Implement the anneal command.

```
function SIMULATED-ANNEALING(problem, schedule) returns a solution State
  current <- problem.INITIAL
  for t = 1 to inf do
      T <- schedule(t)
      if T = 0 then return current
      next <- a randomly selected successor of current
      delta_E <- VALUE(current) - VALUE(next)
      if delta_E > 0 then current <- next
      else current <- next only with probability e^(-delta_E/T)
```

Stuart Russel, Peter Norvig. "Artificial Intelligence: A Modern Approach, 4th Edition" (2021)
"""
import numpy as np

from typing import Callable
try:
    import matplotlib.pyplot as plt
    import networkx as nx
except ModuleNotFoundError:
    plt = None
    nx = None

from ..core.logger import logger
from ..model.problem import ProblemGraph
from ..model.node import Neuron


def _anneal_step(problem:ProblemGraph, T:float, current:Neuron, successor:Neuron) -> Neuron:
    """ Execute one step of the simulated annealing function.
    
    :param problem: The problem definition.
    :type problem: ProblemGraph
    :param T: Current temperature.
    :type T: float
    :param current: The current node, searching for a greener pasture.
    :type current: Neuron
    :param successor: One of the neighboring nodes, enticing.
    :type successor: Neuron
    :return: Either the current or successor node
    :rtype: Neuron
    """
    delta_E = problem.evaluate_node(current) - problem.evaluate_node(successor)
    logger.debug(delta_E)
    if delta_E > 0:
        logger.debug("Taking successor as better option (exploitation)")
        problem.add(successor, current) # Trace the path
        return successor
    else:
        logger.debug(T)
        probability = np.exp(delta_E / T)
        if np.random.default_rng().uniform() < probability:
            logger.debug("Taking successor with probability %d%s (exploration)", probability*100, '%')
            problem.add(successor, current) # Trace the path
            return successor
    return current


def main(problem:ProblemGraph|None=None, schedule:Callable=lambda x : x / 1.002) -> ProblemGraph:
    """ Execute the simulated annealing algorithm.
    
    :param problem: The problem definition.
    :type problem: ProblemGraph
    :param schedule: Temperature function
    :type schedule: Callable
    :return: The problem with solution search graph.
    :rtype: ProblemGraph
    """
    logger.debug("executing anneal command")
    assert problem is None or type(problem) == ProblemGraph
    if problem is None:
        problem = ProblemGraph(Neuron(0, 0, 0))
    if schedule is None:
        schedule = lambda x : x / 1.2
    current = problem.initial
    logger.debug("Initial: %s", current)
    T = 1
    for t in range(10000000):
        T = schedule(T)
        if T < 0.00000001: break
        successor = Neuron(*current.weights + np.random.default_rng().uniform(low=-2.-current.error, high=2.+current.error, size=Neuron.DIM_W))
        current = _anneal_step(problem, T, current, successor)
    static_order = problem.static_order()
    #logger.debug(f"Static Order: {tuple(static_order)}")
    logger.info("Winner: %s", current)
    logger.info("Path Length: %s", len(problem.graph.keys()))
    #logger.debug("graph: %s", problem.graph)
    if plt is not None and nx is not None:
        G = nx.DiGraph()
        for v, e, in problem.graph.items():
            logger.error("%s: %s", v,e)
    return problem


if __name__ == "__main__":
    main()
