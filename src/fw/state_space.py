from dataclasses import dataclass
from typing import Union

from src.fw import State, Operator
from src.fw.algorithms import Algorithm, find


@dataclass
class StateSpace:
    """"""

    initial_state: State
    goal_state: State
    operators: tuple[Operator]
    algorithm: Union[Algorithm, str]

    def solve(self) -> State:
        """"""
        algo = find(self.algorithm)
        return algo.solve(
            self.initial_state,
            self.goal_state,
            self.operators
        )
