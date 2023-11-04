from random import choice, randint
from typing import Union, Iterable
from enum import Enum

# Small numbers from 1 to 10
from src.problems.countdown.countdown_definition import AvailableNumbers

_SMALLS = [num + 1 for num in range(10)]

# Big numbers
_BIGS = [25, 50, 75, 100]


class NumbersType(Enum):
    """This enumeration is meant to be used to prepare a random set of numbers
    by predefined scheme.

    The defined scheme is based on 6 numbers of two types:
        - small numbers [1-10]
        - big numbers {25, 50, 75, 100}

    Each instance represents one common distribution of number types.
    """
    ALL_SMALL = (6, 0)
    ONE_BIG = (5, 1)
    TWO_BIG = (4, 2)
    THREE_BIG = (3, 3)
    FOUR_BIG = (4, 2)

    def __init__(self, n_smalls: int, n_bigs: int):
        super().__init__()
        self.__n_smalls = n_smalls
        self.__n_bigs = n_bigs

    @property
    def n_smalls(self) -> int:
        """Returns the number of small numbers"""
        return self.__n_smalls

    @property
    def n_bigs(self) -> int:
        """Returns the number of big numbers"""
        return self.__n_bigs

    def generate(self) -> tuple[int]:
        """Tries to generate a tuple of numbers by this scheme.
        """
        smalls: list[int] = [choice(_SMALLS) for _ in range(self.n_smalls)]
        bigs: list[int] = [choice(_BIGS) for _ in range(self.n_bigs)]
        all_set = smalls + bigs
        return tuple(all_set)


def generate_countdown_board(
        goal_number: Union[int, None] = None,
        numbers_type: Union[NumbersType, None] = None,
        numbers: Union[Iterable[int], None] = None
) -> tuple[AvailableNumbers, int]:
    """Generates the Countdown board.

    :param goal_number:
        Goal number the algorithm should achieve by applying the mathematical
        operations. When None, it selects it randomly from range [100, 1000].

    :param numbers_type:
        Type of numbers generator. Either this parameter or the `numbers` has
        to be provided, otherwise it raises an error.

    :param numbers:
        An iterable of integers predefining the set of numbers to be played
        with. Either this parameter or the `numbers_type` has to be provided,
        otherwise it raises an error.
    """
    result_numbers: tuple[int] = ()

    if numbers:
        result_numbers = tuple(numbers)
    elif numbers_type:
        result_numbers = numbers_type.generate()

    if not result_numbers:
        raise ValueError(
            f"You have to either specify generator or numbers itself")

    goal_number = goal_number if goal_number else randint(100, 1000)

    return AvailableNumbers(result_numbers), goal_number
