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
from typing import Callable
import numpy as np

from ..core.logger import logger
from ..model.problem import ProblemGraph
from ..model.node import Neuron


def main(problem:ProblemGraph|None=None, schedule:Callable=lambda x : x / 1.2) -> tuple[int]:
    """ Execute the simulated annealing function.
    
    :param problem: The problem definition.
    :type problem: ProblemGraph
    :param schedule: Temperature function
    :type schedule: Callable
    :return: Greeting for the user.
    :rtype: str
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
    for t in range(100000):
        T = schedule(T)
        if T < 0.0001: break
        successor = Neuron(*current.weights + np.random.default_rng().uniform(low=-2., high=2., size=Neuron.DIM_W))
        problem.add(successor, current)
        delta_E = problem.evaluate_node(current) - problem.evaluate_node(successor)
        logger.debug(delta_E)
        if delta_E > 0:
            logger.info("Taking successor as better option (exploitation)")
            current = successor
        else:
            probability = np.exp(delta_E / T)
            if np.random.default_rng().uniform() < probability:
                logger.info("Taking successor with probability %d%s (exploration)", probability*100, '%')
                current = successor
    logger.info("Winner: %s", current)
    return f"Anneal, {tuple(problem.static_order())}!"


