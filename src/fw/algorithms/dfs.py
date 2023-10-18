from src.fw import State
from src.fw.algorithms.base import BlindAlgorithm


class DepthFirstSearch(BlindAlgorithm):

    def __init__(self):
        super().__init__("DFS")

    def next_state(self) -> State:
        """Return the last item (LIFO - stack)"""
        return self.pop_from_fringe(-1)
