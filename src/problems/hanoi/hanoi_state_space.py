import time
from typing import Union

from src.fw import State, Operator, StateSpace
from src.problems.hanoi.hanoi_definition import (
    HanoiSticks, Stick, initialize_hanoi_sticks)


class HanoiState(State):

    def __init__(
            self,
            hanoi_sticks: HanoiSticks,
            parent: Union["HanoiState", None] = None,
            applied_operator: Union["Operator", None] = None
    ):
        super().__init__(parent, applied_operator)
        self.__hanoi_sticks = hanoi_sticks

    @property
    def hanoi_sticks(self) -> HanoiSticks:
        return self.__hanoi_sticks

    def has_stick(self, stick_index: int) -> bool:
        return self.hanoi_sticks.stick_by_index(stick_index) is not None

    def stick(self, stick_index: int) -> Stick:
        return self.hanoi_sticks.stick_by_index(stick_index)

    def distance_from(self, state: "HanoiState") -> float:
        n_all_disks = len(state.hanoi_sticks.disks)
        n_goal_disks = state.hanoi_sticks.goal_stick.n_disks

        return n_all_disks - n_goal_disks

    def __eq__(self, other: "HanoiState") -> bool:
        self_disk_distribution = self.hanoi_sticks.sticks
        other_disk_distribution = other.hanoi_sticks.sticks

        return self_disk_distribution == other_disk_distribution

    def __repr__(self):
        return f"{self.hanoi_sticks}"


class MoveOperator(Operator):

    def __init__(self, from_stick: int, to_stick: int):
        super().__init__(f"{from_stick} -> {to_stick}")
        self.__from_stick = from_stick
        self.__to_stick = to_stick

    @property
    def from_stick(self) -> int:
        return self.__from_stick

    @property
    def to_stick(self) -> int:
        return self.__to_stick

    def can_be_applied(self, state: HanoiState) -> bool:
        f_stick = state.stick(self.from_stick)
        t_stick = state.stick(self.to_stick)

        # If any of the sticks is missing
        if (not f_stick) or (not t_stick):
            return False

        # If the from_stick doesn't have any disk to move
        if not f_stick.has_any_disk:
            return False

        # Return if can be the top disk moved to the to_stick
        return t_stick.can_stack(f_stick.top_disk)

    def apply(self, state: HanoiState) -> HanoiState:
        new_hanoi = state.hanoi_sticks.clone

        f_stick = new_hanoi.stick_by_index(self.from_stick)
        t_stick = new_hanoi.stick_by_index(self.to_stick)

        disk = f_stick.pop_top_disk()

        t_stick.add_disk(disk)

        return HanoiState(
            hanoi_sticks=new_hanoi,
            parent=state,
            applied_operator=self
        )


n_sticks = 4
n_disks = 5

operators = []

init, goal = initialize_hanoi_sticks(n_sticks, n_disks)

for idx, from_stick in enumerate(init.sticks):
    for to_stick in init.sticks:
        if from_stick != to_stick:
            operators.append(MoveOperator(from_stick.index, to_stick.index))

init_state, goal_state = HanoiState(init), HanoiState(goal)

print(init.sticks)

for algo in ["DFS", "BFS", "GREEDY", "A_STAR", "GRADIENT"]:

    print(100 * "=")
    print("Trying algorithm:", algo)

    ss = StateSpace(
        initial_state=init_state,
        goal_state=goal_state,
        operators=operators,
        algorithm=algo
    )

    start = time.time()

    solved = ss.solve()

    end = time.time()

    applied = solved.all_applied_operators(reverse_operators=True)
    print(len(applied), applied)
    print(end - start, "seconds")

