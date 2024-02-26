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
from ..core.logger import logger
from ..model.problem import ProblemGraph
from ..model.node import Neuron


def main(problem:ProblemGraph|None=None, schedule:None=None) -> tuple[int]:
    """ Execute the simulated annealing function.
    
    :param problem: name to use in greeting
    :type problem: ProblemGraph
    :param schedule: name to use in greeting
    :type schedule: Any
    :return: Greeting for the user.
    :rtype: str
    """
    logger.debug("executing anneal command")
    assert problem is None or type(problem) == ProblemGraph
    if problem is None:
        problem = ProblemGraph({
            Neuron(0, 0, 0): {Neuron(1, 0, 1)},
            Neuron(1, 0, 1): {Neuron(1, 0, 1)},
            Neuron(-1, -1, 0): {Neuron(1, 0, 1)}
        })
    return f"Anneal, {problem}!"


