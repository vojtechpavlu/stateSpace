from dataclasses import dataclass
from typing import Iterable


@dataclass
class Disk:
    """"""
    size: int

    @property
    def clone(self) -> "Disk":
        return Disk(self.size)


class Stick:
    """"""
    def __init__(self, index: int, disks: Iterable[Disk] = ()):
        self.__index = index
        self.__disks: list[Disk] = list(sorted(disks, key=lambda d: d.size))

    @property
    def index(self) -> int:
        return self.__index

    @property
    def disks(self) -> tuple[Disk]:
        return tuple(self.__disks)

    @disks.setter
    def disks(self, new_disks: Iterable[Disk]):
        self.__disks = list(sorted(new_disks, key=lambda d: d.size))

    @property
    def top_disk(self) -> Disk:
        return min(self.disks, key=lambda d: d.size)

    @property
    def n_disks(self) -> int:
        return len(self.disks)

    @property
    def has_any_disk(self) -> bool:
        return self.n_disks > 0

    @property
    def clone(self) -> "Stick":
        return Stick(self.index, [d.clone for d in self.disks])

    @property
    def sizes(self) -> tuple[int]:
        return tuple([d.size for d in self.disks])

    def can_stack(self, disk: Disk) -> bool:
        return (not self.has_any_disk) or (self.top_disk.size > disk.size)

    def add_disk(self, disk: Disk):
        """"""
        if not self.can_stack(disk):
            raise IllegalOperation(
                f"Disk to be put on top of the stick has to be smaller: "
                f"to be put: {disk.size}, top disk: {self.top_disk.size}")

        self.disks = [*self.disks, disk]

    def pop_top_disk(self) -> Disk:
        """"""
        if not self.has_any_disk:
            raise IllegalOperation(f"There's no disk at the stick")

        top_disk = self.top_disk
        self.__disks.remove(self.top_disk)
        return top_disk

    def __repr__(self):
        return f"{self.index} {self.disks}"

    def __eq__(self, other: "Stick") -> bool:
        return self.disks == other.disks


class HanoiSticks:
    """"""

    def __init__(self, sticks: Iterable[Stick]):
        self.__sticks: list[Stick] = list(sticks)

    @property
    def sticks(self) -> tuple[Stick]:
        return tuple(self.__sticks)

    @property
    def n_sticks(self) -> int:
        return len(self.sticks)

    @property
    def clone(self) -> "HanoiSticks":
        return HanoiSticks([s.clone for s in self.sticks])

    @property
    def start_stick(self) -> Stick:
        return self.sticks[0]

    @property
    def goal_stick(self) -> Stick:
        return self.sticks[-1]

    @property
    def disks(self) -> tuple[Disk]:
        disks = []

        for stick in self.sticks:
            disks.extend(stick.disks)

        return tuple(disks)

    @property
    def disk_sizes(self) -> tuple[int]:
        return tuple(self.disks)

    def stick_by_index(self, stick_index: int) -> Stick:
        for stick in self.sticks:
            if stick.index == stick_index:
                return stick

    def __repr__(self):
        return f"{tuple([repr(s) for s in self.sticks])}"


class IllegalOperation(Exception):
    """"""

    def __init__(self, message: str):
        Exception.__init__(self, message)
        self.__message = message

    @property
    def message(self) -> str:
        return self.__message


def _initialize(
        disks_on_stick_idx: int,
        n_sticks: int = 3,
        n_disks: int = 5
) -> HanoiSticks:
    sticks = []

    for stick_index in range(n_sticks):
        sticks.append(Stick(stick_index))

    for disk_size in range(n_disks - 1, 0, -1):
        sticks[disks_on_stick_idx].add_disk(Disk(disk_size))

    return HanoiSticks(sticks)


def initialize_hanoi_sticks(
        n_sticks: int = 3,
        n_disks: int = 5
) -> tuple[HanoiSticks, HanoiSticks]:
    """"""
    return (
        _initialize(0, n_sticks, n_disks),
        _initialize(-1, n_sticks, n_disks)
    )
