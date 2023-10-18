from random import choice

from src.fw import State, Operator
from src.fw.algorithms import Algorithm
from src.fw.algorithms.base import NoSolutionFound


class Random(Algorithm):

    def next_state(self):
        """Unused in this case"""
        pass

    def __init__(self, limit: int = 10_000):
        super().__init__("RANDOM")
        self.__limit = limit

    @property
    def limit(self) -> int:
        return self.__limit

    def solve(
            self,
            initial_state: State,
            goal_state: State,
            operators: tuple[Operator]
    ) -> State:
        counter = 0
        current = initial_state

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