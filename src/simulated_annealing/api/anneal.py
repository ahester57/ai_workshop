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

Stuart Russel, Peter Norvig. 'Artificial Intelligence: A Modern Approach, 4th Edition' (2021)
"""
import networkx as nx
import numpy as np

from graphlib import CycleError
from typing import Callable

try:
    # for visual mode. `pip install -e .[visual]`
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None

from ..core.logger import logger
from ..model.problem import ProblemGraph
from ..model.node import Neuron


# Graphing Flags
GRAPH_TEMP = True
GRAPH_OBJECTIVE = True
GRAPH_DELTA_E = True

NUM_RANDOM_RESTARTS=5


def _anneal_step(
        problem:ProblemGraph,
        T:float,
        current:Neuron,
        successor:Neuron
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
    :return: Next node, evaluation of next, delta_E
    :rtype: Neuron, float, float
    """
    e_value = problem.evaluate_node(successor)
    delta_E = problem.evaluate_node(current) - e_value
    # logger.debug(f'delta_E: {delta_E}')
    # logger.debug(f'e_value: {e_value}')
    if delta_E > 0:
        logger.debug('Taking better successor (exploitation)')
        problem.add(successor, current) # Trace the path
        return successor, e_value, delta_E
    else:
        logger.debug(T)
        probability = np.exp(delta_E / T)
        if np.random.default_rng().uniform() < probability:
            logger.debug('Taking worse successor with probability %d%s (exploration)', probability*100, '%')
            problem.add(successor, current) # Trace the path
            return successor, e_value, delta_E
    return current, e_value, delta_E


def _anneal_loop(
        problem:ProblemGraph|None=None,
        schedule:Callable=lambda x : x / 1.2
    ) -> Neuron:
    """ Execute the simulated annealing algorithm.
    
    :param problem: The problem definition.
    :type problem: ProblemGraph
    :param schedule: Temperature function
    :type schedule: Callable
    :return: The winner
    :rtype: Neuron
    """
    logger.debug('executing anneal command')
    assert isinstance(problem, ProblemGraph)
    assert isinstance(schedule, Callable)
    current = problem.initial
    logger.debug('Initial: %s', current)
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
        current, e_value, delta_E = _anneal_step(problem, T, current, successor)
        if GRAPH_OBJECTIVE:
            eval_history.append(e_value)
        if GRAPH_OBJECTIVE:
            delta_history.append(delta_E)
    if current.error > 0.5:
        logger.warning('Skipping erroneous result')
        return current
    if GRAPH_TEMP:
        logger.info(f'Temp over Time: {T_history}')
        if plt is not None:
            steps = np.arange(1, len(T_history)+1)
            plt.plot(steps, T_history, marker='o')
            plt.title('Temperature over Time')
            plt.xlabel('Step')
            plt.ylabel('Temperature Value')
            plt.show()
    if GRAPH_OBJECTIVE:
        logger.info(f'Obj Fn. over Time: {eval_history}')
        if plt is not None:    
            steps = np.arange(1, len(eval_history)+1)
            plt.plot(steps, eval_history, marker='o')
            plt.title('Objective Fn. over Time')
            plt.xlabel('Step')
            plt.ylabel('Objection Fn. Value')
            plt.show()
    if GRAPH_DELTA_E:
        logger.info(f'Delta E over Time: {delta_history}')
        if plt is not None:
            steps = np.arange(1, len(delta_history)+1)
            plt.plot(steps, delta_history, marker='o')
            plt.title('Delta E over Time')
            plt.xlabel('Step')
            plt.ylabel('Delta E Value')
            plt.show()
    return current


def main(draw:bool=False, schedule:Callable=lambda x : x / 1.2) -> ProblemGraph:
    """ Entrypoint to the simulated annealing algorithm.
    
    :param draw: Whether or not to draw the graphs. Disabled is visual not installed.
    :type draw: bool
    :param schedule: Temperature function
    :type schedule: Callable
    :return: The problem with solution search graph.
    :rtype: ProblemGraph
    """
    logger.debug('executing anneal command')
    assert schedule is None or isinstance(schedule, Callable)
    global plt
    if not draw:
        plt = None
        logger.warning('not drawing graphs')
    elif plt is None:
        logger.warning('--draw flag given but visual mode not installed. `pip install -e .[visual]`')
    problem = ProblemGraph(Neuron(0, 0, 0))
    if schedule is None:
        schedule = lambda x : x / 1.2
    for attempt in range(1, NUM_RANDOM_RESTARTS+1):
        # Run simulated annealing
        # Random Restarts NUM_RANDOM_RESTARTSx or until err < 0.5
        winner = _anneal_loop(problem, schedule)
        try:
            # Topological sort
            static_order = tuple(problem.static_order())
        except CycleError as cycerr:
            logger.warn(cycerr)
            static_order = 'cycle detected'
        logger.info(f'Winner#[{attempt}] -- {winner}')
        logger.info('Path Length: %s', len(problem.graph.keys()))
        if winner.error < 0.5:
            logger.info(f'Acceptable winner found on attempt #{attempt}')
            logger.info(f'Static Order: {static_order}')
            break
        if attempt == NUM_RANDOM_RESTARTS:
            logger.info(f'Giving up search after {attempt} attempt(s).')
            break;
        logger.warning(f'Winner not good enough, restarting with attempt #{attempt+1}.')
        problem = ProblemGraph(Neuron(0, 0, 0))
    logger.info(f'Graph Length: {len(problem.diGraph)}')
    logger.info(f'Adjacency data: {nx.adjacency_data(problem.diGraph)}')
    if plt is not None:
        pos = nx.kamada_kawai_layout(problem.diGraph, weight=None)
        nx.draw(problem.diGraph, pos, with_labels=True, node_color='blue', edge_color='grey', node_size=20)
        plt.show()
    return problem


if __name__ == '__main__':
    main()
