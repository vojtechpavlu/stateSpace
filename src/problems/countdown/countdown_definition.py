from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class AvailableNumbers:
    numbers: tuple[int]

    def __len__(self) -> int:
        return len(self.numbers)

    def __repr__(self) -> str:
        return f"{self.numbers}"


class NumberOperation(ABC):

    def __init__(self, sign: str):
        self.__sign = sign

    @property
    def sign(self) -> str:
        """"""
        return self.__sign

    @abstractmethod
    def process(self, number1: int, number2: int) -> int:
        """"""

    @abstractmethod
    def can_be_used(self, number1: int, number2: int) -> bool:
        """"""

    def stringify(self, number1: int, number2: int) -> str:
        """"""
        return f"{number1} {self.sign} {number2}"


class Addition(NumberOperation):

    def __init__(self):
        super().__init__("+")

    def process(self, number1: int, number2: int) -> int:
        return number1 + number2

    def can_be_used(self, number1: int, number2: int) -> bool:
        return True


class Subtraction(NumberOperation):

    def __init__(self):
        super().__init__("-")

    def process(self, number1: int, number2: int) -> int:
        return number1 - number2

    def can_be_used(self, number1: int, number2: int) -> bool:
        return number1 > number2


class Multiplication(NumberOperation):

    def __init__(self):
        super().__init__("*")

    def process(self, number1: int, number2: int) -> int:
        return number1 * number2

    def can_be_used(self, number1: int, number2: int) -> bool:
        return True


class Division(NumberOperation):

    def __init__(self):
        super().__init__("/")

    def process(self, number1: int, number2: int) -> int:
        return number1 * number2

    def can_be_used(self, number1: int, number2: int) -> bool:
        """"""
        return number2 != 0 and number1 % number2 == 0


_number_operations: tuple[NumberOperation] = (
    Addition(), Subtraction(), Multiplication(), Division()
)


def number_operations() -> tuple[NumberOperation]:
    """"""
    return _number_operations
