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

from graphlib import CycleError
from typing import Callable

try:
    # for visual mode. `pip install -e .[visual]
    import matplotlib.pyplot as plt
    import networkx as nx
    DiGraph = nx.DiGraph
except ModuleNotFoundError:
    plt = None
    nx = None
    class DiGraph: pass

from ..core.logger import logger
from ..model.problem import ProblemGraph
from ..model.node import Neuron


# Graphing Flags
GRAPH_TEMP = True
GRAPH_OBJECTIVE = True
GRAPH_DELTA_E = True


def _anneal_step(
        problem:ProblemGraph,
        T:float,
        current:Neuron,
        successor:Neuron,
        G:DiGraph|None=None
    ) -> Neuron:
    """ Execute one step of the simulated annealing function.
    
    :param problem: The problem definition.
    :type problem: ProblemGraph
    :param T: Current temperature.
    :type T: float
    :param current: The current node, searching for a greener pasture.
    :type current: Neuron
    :param successor: One of the neighboring nodes, enticing.
    :type successor: Neuron
    :param G: The network graph, if visual mode enabled.
    :type G: networkx.DiGraph|None
    :return: Next node, evaluation of next, delta_E
    :rtype: Neuron, float, float
    """
    e_value = problem.evaluate_node(successor)
    delta_E = problem.evaluate_node(current) - e_value
    logger.debug(f"delta_E: {delta_E}")
    logger.debug(f"e_value: {e_value}")
    if delta_E > 0:
        logger.debug("Taking successor as better option (exploitation)")
        problem.add(successor, current) # Trace the path
        if G is not None:
            G.add_edge(current, successor)
        return successor, e_value, delta_E
    else:
        logger.debug(T)
        probability = np.exp(delta_E / T)
        if np.random.default_rng().uniform() < probability:
            logger.debug("Taking successor with probability %d%s (exploration)", probability*100, '%')
            problem.add(successor, current) # Trace the path
            if G is not None:
                G.add_edge(current, successor)
            return successor, e_value, delta_E
    return current, e_value, delta_E


def _anneal_loop(
        problem:ProblemGraph|None=None,
        schedule:Callable=lambda x : x / 1.2,
        G:DiGraph|None=None
    ) -> Neuron:
    """ Execute the simulated annealing algorithm.
    
    :param problem: The problem definition.
    :type problem: ProblemGraph
    :param schedule: Temperature function
    :type schedule: Callable
    :param G: The network graph, if visual mode enabled.
    :type G: networkx.DiGraph|None
    :return: The winner
    :rtype: Neuron
    """
    logger.debug("executing anneal command")
    assert isinstance(problem, ProblemGraph)
    assert isinstance(schedule, Callable)
    current = problem.initial
    logger.debug("Initial: %s", current)
    if GRAPH_TEMP:
        T_history = []
    if GRAPH_OBJECTIVE:
        eval_history = []
    if GRAPH_DELTA_E:
        delta_history = []
    T = 1
    for t in range(10000000):
        if GRAPH_TEMP:
            T_history.append(T)
        T = schedule(T)
        if T < 0.000000001: break
        successor = Neuron(
            *current.weights
           + np.random.default_rng()
                .integers(
                    low=-2.-current.error,
                   # widen step size as error increases
                    high=2.+current.error,
                    size=Neuron.DIM_W)
        )
        current, e_value, delta_E = _anneal_step(problem, T, current, successor, G)
        if GRAPH_OBJECTIVE:
            eval_history.append(e_value)
        if GRAPH_OBJECTIVE:
            delta_history.append(delta_E)
    if current.error > 0.5:
        return current
    if G is not None and GRAPH_TEMP:
        steps = np.arange(1, len(T_history)+1)
        plt.plot(steps, T_history, marker='o')
        plt.title("Temperature over Time")
        plt.xlabel("Step")
        plt.ylabel("Temperature Value")
        plt.show()
    if G is not None and GRAPH_OBJECTIVE:
        steps = np.arange(1, len(eval_history)+1)
        plt.plot(steps, eval_history, marker='o')
        plt.title("Objective Fn. Value over Time")
        plt.xlabel("Step")
        plt.ylabel("Objection Fn. Value")
        plt.show()
    if G is not None and GRAPH_DELTA_E:
        steps = np.arange(1, len(delta_history)+1)
        plt.plot(steps, delta_history, marker='o')
        plt.title("Delta E Value over Time")
        plt.xlabel("Step")
        plt.ylabel("Delta E Value")
        plt.show()
    return current


def main(problem:ProblemGraph|None=None, schedule:Callable=lambda x : x / 1.22) -> ProblemGraph:
    """ Entrypoint to the simulated annealing algorithm.
    
    :param problem: The problem definition.
    :type problem: ProblemGraph
    :param schedule: Temperature function
    :type schedule: Callable
    :return: The problem with solution search graph.
    :rtype: ProblemGraph
    """
    logger.debug('executing anneal command')
    assert problem is None or isinstance(problem, ProblemGraph)
    assert schedule is None or isinstance(schedule, Callable)
    if problem is None:
        problem = ProblemGraph(Neuron(0, 0, 0))
    if schedule is None:
        schedule = lambda x : x / 1.2
    for attempt in range(1, 100):
        # Random Restarts 100x or until err < 0.5
        G = None
        if plt is not None and nx is not None:
            G = nx.DiGraph()
        # Run simulated annealing
        winner = _anneal_loop(problem, schedule, G)
        try:
            # Topological sort
            static_order = tuple(problem.static_order())
        except CycleError as cycerr:
            logger.warn(cycerr)
            static_order = 'cycle'
        logger.debug(f"Static Order: {static_order}")
        logger.info("Winner: %s", winner)
        logger.info("Path Length: %s", len(problem.graph.keys()))
        if winner.error < 0.5:
            break
        logger.warn("Winner not good enough, restarting with attempt #%d.", attempt)
        problem = ProblemGraph(Neuron(0, 0, 0))
    if G is not None:
        logger.info("Graph Length: %s", len(G))
        pos = nx.kamada_kawai_layout(G, weight=None)
        nx.draw(G, pos, with_labels=True, node_color='blue', edge_color='grey', node_size=20)
        plt.show()
    return problem


if __name__ == "__main__":
    main()
