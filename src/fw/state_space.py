from typing import Iterable
from dataclasses import dataclass
from typing import Union

from src.fw import State, Operator
from src.fw.algorithms import Algorithm, find


@dataclass
class StateSpace:
    """Instances of this class tries to provide a simple facade to use and
    manage the State Space API.

    State Space initor takes the following parameters:
        - `initial_state`: `State`
            State the algorithm should be seeking the path from

        - `goal_state`: `State`
            State the algorithm should find the path to

        - `operators`: `Iterable[Operator]`
            Available operators the algorithm can use

        - `algorithm`: `Union[Algorithm, str]`
            Algorithm to be used to search in a graph
    """

    initial_state: State                # Root of the State Space Tree
    goal_state: State                   # Desired leaf of the State Space Tree
    operators: Iterable[Operator]       # Available operators to be used
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
            tuple(self.operators)
        )
