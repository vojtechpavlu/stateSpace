"""This package contains definitions of all the implemented algorithms used to
search in the graph (State Space).
"""

from typing import Union

from src.fw.algorithms.base import Algorithm
from src.fw.algorithms.bfs import BreadthFirstSearch
from src.fw.algorithms.dfs import DepthFirstSearch
from src.fw.algorithms.greedy import GreedySearch
from src.fw.algorithms.a_star import AStar
from src.fw.algorithms.random_algo import FullRandom


def algorithms() -> tuple[Algorithm]:
    """Returns the whole set of implemented algorithms.
    """
    return tuple([
        # Blind algorithms
        DepthFirstSearch(),
        BreadthFirstSearch(),

        # Heuristic algorithms
        GreedySearch(),
        AStar(),

        # Random algorithms
        # Random()
    ])


def algorithm_names() -> tuple[str]:
    """Returns names of all the algorithms."""
    return tuple([algo.name for algo in algorithms()])


def find_by_name(name: str) -> Algorithm:
    """Tries to find algorithm by the given name. When there is no such
    algorithm found, it raises an error. Function is case-insensitive.
    """
    for algorithm in algorithms():
        if algorithm.name.upper() == name.upper():
            return algorithm
    raise NoSuchAlgorithmError(f"No algorithm '{name}' found")


def find(algorithm: Union[Algorithm, str]) -> Algorithm:
    """Tries to find an algorithm. The input can be either a string (name of
    the algorithm) or the algorithm itself. When dealing with names, it is
    case-insensitive. When using some other type, it raises an error.
    """
    if isinstance(algorithm, Algorithm):
        return algorithm
    elif isinstance(algorithm, str):
        return find_by_name(algorithm.upper())
    else:
        ValueError(f"Unrecognized algorithm type: '{type(algorithm)}'")


class NoSuchAlgorithmError(Exception):
    """Error used when the desired algorithm is not found."""
