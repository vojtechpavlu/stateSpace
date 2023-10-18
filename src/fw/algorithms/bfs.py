from src.fw import State
from src.fw.algorithms.base import BlindAlgorithm


class BreadthFirstSearch(BlindAlgorithm):

    def __init__(self):
        super().__init__("BFS")

    def next_state(self) -> State:
        """Return the first item (FIFO - queue)"""
        return self.pop_from_fringe(0)

