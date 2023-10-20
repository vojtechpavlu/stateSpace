from src.fw import State
from src.fw.algorithms.base import Algorithm


class GreedySearch(Algorithm):
    """Simple implementation of a heuristic algorithm based on
    a nearest-neighbour decisioning.
    """

    def __init__(self):
        super().__init__("GREEDY")

    def next_state(self) -> State:
        """Return the state closest to the goal state.
        This method expects the goal state is already set. When it isn't,
        it raises an error.
        """
        if not self.goal_state:
            raise Exception("Goal state wasn't set yet")

        # Helper function
        def comparison(state):
            """Return a distance between the given state and the goal.
            """
            return state.distance_from(self.goal_state)

        # Find the state in fringe that is closest to the goal
        closest = min(self.fringe, key=comparison)
        self.drop_from_fringe(closest)
        return closest

    # def solve(self, initial_state: State, goal_state: State,
    #           operators: tuple[Operator]) -> State:
    #     """Implementation of the actual algorithm."""
    #     self.__fringe.append(initial_state)
    #
    #     while len(self.fringe) > 0:
    #         current = self.next_state()
    #
    #         if current == goal_state:
    #             return current
    #
    #         if current in self.closed:
    #             continue
    #
    #         for operator in operators:
    #             if operator.can_be_applied(current):
    #                 self.__fringe.append(operator.apply(current))
    #         self.__closed.append(current)
    #
    #     raise NoSolutionFound()

