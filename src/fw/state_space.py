from dataclasses import dataclass
from typing import Union

from src.fw import State, Operator
from src.fw.algorithms import Algorithm, find


@dataclass
class StateSpace:
    """Instances of this class tries to provide a simple facade to use and
    manage the State Space API.
    """

    initial_state: State                # Root of the State Space Tree
    goal_state: State                   # Desired leaf of the State Space Tree
    operators: tuple[Operator]          # Available operators to be used
    algorithm: Union[Algorithm, str]    # Algorithm to be used to search

    def solve(self) -> State:
        """Simple method scheduling the steps to find a solution.
        The received solution is based on a state equivalent with the goal
        with addition of the whole path from the initial state.
        """
        algo = find(self.algorithm)
        algo.goal_state = self.goal_state

        return algo.solve(
            self.initial_state,
            self.goal_state,
            self.operators
        )
