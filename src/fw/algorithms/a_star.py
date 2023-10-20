from src.fw import State, Operator
from src.fw.algorithms.base import Algorithm, NoSolutionFound


class AStar(Algorithm):
    """"""

    def __init__(self):
        super().__init__("A_STAR")
        self.__fringe: list[State] = []
        self.__closed: list[State] = []

    @property
    def fringe(self) -> tuple[State]:
        return tuple(self.__fringe)

    @property
    def closed(self) -> tuple[State]:
        return tuple(self.__closed)

    def next_state(self):
        """Tries to find a best state considering both path length from the
        beginning and a lower bound estimate of a cost to get to the goal
        state."""

        # Find the best state to search in and remove it from fringe
        best = min(self.fringe, key=self._g_plus_h)
        self.__fringe.remove(best)
        return best

    def _g_plus_h(self, state: State) -> float:
        """Helper function to evaluate a state to a float by a cost to
        get to the current state (g) and a lower-bound cost estimate to
        get from it to the goal state (h).
        """
        g = len(state.all_applied_operators())
        h = state.distance_from(self.goal_state)
        return g + h

    def solve(
            self,
            initial_state: State,
            goal_state: State,
            operators: tuple[Operator]
    ) -> State:
        self.__fringe.append(initial_state)

        while len(self.fringe) > 0:
            current = self.next_state()

            if current == goal_state:
                return current

            if current in self.closed:
                continue

            for operator in operators:
                if operator.can_be_applied(current):
                    descendant = operator.apply(current)
                    if descendant not in self.__fringe:
                        self.__fringe.append(descendant)
            self.__closed.append(current)

        raise NoSolutionFound()

