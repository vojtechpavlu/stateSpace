from typing import Union

from src.fw.algorithms.base import Algorithm
from src.fw.algorithms.bfs import BreadthFirstSearch
from src.fw.algorithms.dfs import DepthFirstSearch
from src.fw.algorithms.random_algo import Random


def algorithms() -> tuple[Algorithm]:
    """"""
    return tuple([
        DepthFirstSearch(),
        BreadthFirstSearch(),

        Random()
    ])


def algorithm_names() -> tuple[str]:
    """"""
    return tuple([algo.name for algo in algorithms()])


def find_by_name(name: str) -> Algorithm:
    """"""
    for algorithm in algorithms():
        if algorithm.name == name:
            return algorithm
    raise NoSuchAlgorithmError(f"No algorithm '{name}' found")


def find(algorithm: Union[Algorithm, str]) -> Algorithm:
    if isinstance(algorithm, Algorithm):
        return algorithm
    elif isinstance(algorithm, str):
        return find_by_name(algorithm)
    else:
        ValueError(f"Unrecognized algorithm type: '{type(algorithm)}'")


class NoSuchAlgorithmError(Exception):
    """"""

    def __init__(self, message: str):
        Exception.__init__(self, message)
        self.__message = message

    @property
    def message(self) -> str:
        return self.__message
