from src.fw import State
from src.fw.algorithms.base import Algorithm


class AStar(Algorithm):
    """A* algorithm is well known for it's ability to use two separate
    heuristic functions to evaluate each node in the graph and using this
    approach it usually finds a very good solution.

    The drawback is that this naive implementation is not optimized for this
    approach and takes longer time to search (due to the nature of the
    parents back-tracking).
    """

    def __init__(self):
        super().__init__("A_STAR")

    def next_state(self):
        """Tries to find a best state considering both path length from the
        beginning and a lower bound estimate of a cost to get to the goal
        state."""

        # Find the best state to search in and remove it from fringe
        best = min(self.fringe, key=self._g_plus_h)
        self.drop_from_fringe(best)
        return best

    def _g_plus_h(self, state: State) -> float:
        """Helper function to evaluate a state to a float by a cost to
        get to the current state (g) and a lower-bound cost estimate to
        get from it to the goal state (h).
        """
        g = len(state.all_parents())
        h = state.distance_from(self.goal_state)
        return g + h
