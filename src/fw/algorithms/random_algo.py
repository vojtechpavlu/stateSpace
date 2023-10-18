from random import choice

from src.fw import State, Operator
from src.fw.algorithms import Algorithm
from src.fw.algorithms.base import NoSolutionFound


class FullRandom(Algorithm):
    """This algorithm is implemented just for the notion of non-systematic
    algorithm and it's drawbacks. It simply tries to go in a random direction
    with no idea if it's returning back or not.

    To prevent it's possible long-running, it's limited in number of states
    it goes through. By default, this limit is set to 10k.
    """

    def next_state(self):
        """Unused in this case"""
        pass

    def __init__(self, limit: int = 10_000):
        super().__init__("FULL_RANDOM")
        self.__limit = limit

    @property
    def limit(self) -> int:
        """Limit of possible searched states."""
        return self.__limit

    def solve(
            self,
            initial_state: State,
            goal_state: State,
            operators: tuple[Operator]
    ) -> State:
        """Naive implementation of a fully random algorithm to search the
        state space.
        """
        counter = 0
        current = initial_state

        # While the limit is not reached, repeat
        while counter < self.limit:

            # When the current state is the desired one
            if current == goal_state:
                return current

            # Select random operator
            available_ops = [o for o in operators if o.can_be_applied(current)]
            randomly_selected = choice(available_ops)

            current = randomly_selected.apply(current)

        # There's no state to be searched in and still no solution found
        raise NoSolutionFound()
