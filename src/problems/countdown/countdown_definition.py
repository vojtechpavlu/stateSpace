"""This module contains a basic definition of the Countdown Numbers problem.
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class AvailableNumbers:
    """A list of numbers to be calculated with."""

    numbers: tuple[int]

    def __len__(self) -> int:
        return len(self.numbers)

    def __repr__(self) -> str:
        return f"{self.numbers}"


class NumberOperation(ABC):
    """Base abstract class defining the protocol of all the available
    mathematical operations you can do with the given numbers.

    The act of application is based on calculating the result of the
    `a ? b`, where the `?` represents the operator itself. Keep in mind that
    some operations are not commutative (`a ? b != b ? a`).
    """

    def __init__(self, sign: str):
        self.__sign = sign

    @property
    def sign(self) -> str:
        """Sign representing the operation."""
        return self.__sign

    @abstractmethod
    def process(self, number1: int, number2: int) -> int:
        """Method processing the given integer numbers resulting in another
        integer."""

    @abstractmethod
    def can_be_used(self, number1: int, number2: int) -> bool:
        """Returns if this operation can be used on the given two numbers.
        Some rules are purely mathematical, others are rooted in the game.
        """

    def stringify(self, number1: int, number2: int) -> str:
        """Tries to stringify the operation with the given numbers."""
        return f"{number1} {self.sign} {number2}"


class Addition(NumberOperation):
    """Addition operation is the most basic operation used in this game.
    It simply adds the two numbers. It also has no restrictions on the given
    numbers - you can add any two numbers.
    """

    def __init__(self):
        super().__init__("+")

    def process(self, number1: int, number2: int) -> int:
        return number1 + number2

    def can_be_used(self, number1: int, number2: int) -> bool:
        return True


class Subtraction(NumberOperation):
    """Subtraction operation simply represents the 'minus' operation.
    Can be applied only when the `a` > `b`.
    """

    def __init__(self):
        super().__init__("-")

    def process(self, number1: int, number2: int) -> int:
        return number1 - number2

    def can_be_used(self, number1: int, number2: int) -> bool:
        return number1 > number2


class Multiplication(NumberOperation):
    """Operation for multiplying the given numbers. This operation is also
    applicable on any two given integer numbers."""

    def __init__(self):
        super().__init__("*")

    def process(self, number1: int, number2: int) -> int:
        return number1 * number2

    def can_be_used(self, number1: int, number2: int) -> bool:
        return True


class Division(NumberOperation):
    """Division - the most complex operation. Not only the mathematics
    restricts available numbers combinations you can use (like `b != 0`),
    the result also cannot result in a fraction (result must be integer),
    which means the `a` must be fully divisible by `b`.
    """

    def __init__(self):
        super().__init__("/")

    def process(self, number1: int, number2: int) -> int:
        return int(number1 / number2)

    def can_be_used(self, number1: int, number2: int) -> bool:
        """`b` cannot be zero and `a` must be divisible by `b`."""
        return number2 != 0 and number1 % number2 == 0


# Accumulate the operations
_number_operations: tuple[NumberOperation] = (
    Addition(), Subtraction(), Multiplication(), Division()
)


def number_operations() -> tuple[NumberOperation]:
    """Returns the tuple of available operations you can use."""
    return _number_operations
