from src.fw import State, Union, Operator
from src.problems.countdown.countdown_definition import (
    AvailableNumbers, NumberOperation)


class CountdownState(State):

    def __init__(
            self,
            available_numbers: AvailableNumbers,
            goal_number: int,
            stringified_operator: str = "",
            parent: Union["State", None] = None,
            applied_operator: Union["CountdownOperator", None] = None
    ):
        State.__init__(self, parent, applied_operator)
        self.__available_numbers = available_numbers
        self.__goal_number = goal_number
        self.__stringified_operator = stringified_operator

    @property
    def available_numbers(self) -> tuple[int]:
        return self.__available_numbers.numbers

    @property
    def goal_number(self) -> int:
        return self.__goal_number

    @property
    def stringified_operator(self) -> str:
        return self.__stringified_operator

    @property
    def stringified_path(self) -> tuple[str]:
        return tuple([p.stringified_operator for p in self.all_parents(True)])

    def distance_from(self, state: "CountdownState") -> float:
        """Returns the distance between the goal number and the closest one
        of the all available numbers."""
        return min([abs(n - self.goal_number) for n in self.available_numbers])

    def __eq__(self, other: "CountdownState") -> bool:
        return (
            sorted(self.available_numbers) == sorted(other.available_numbers)
        )

    def is_terminal_state(self, goal_state: "State") -> bool:
        """This method is overridden to enhance the ability to check the
        terminal state.
        """
        return self.goal_number in self.available_numbers


class CountdownOperator(Operator):

    def __init__(
        self,
        number_operation: NumberOperation,
        a_idx: int,
        b_idx: int
    ):
        super().__init__(number_operation.sign)
        self.__number_operation = number_operation
        self.__a_idx = a_idx
        self.__b_idx = b_idx

        if a_idx == b_idx:
            raise ValueError(f"Cannot have same indexes: {a_idx=}, {b_idx=}")

    @property
    def number_operation(self) -> NumberOperation:
        return self.__number_operation

    @property
    def indexes(self) -> tuple[int, int]:
        return self.__a_idx, self.__b_idx

    def can_be_applied(self, state: CountdownState) -> bool:
        nums = state.available_numbers
        a_idx, b_idx = self.indexes

        if len(nums) > a_idx and len(nums) > b_idx:
            a, b = nums[a_idx], nums[b_idx]
            return self.number_operation.can_be_used(a, b)

        return False

    def apply(self, state: CountdownState) -> CountdownState:
        nums = state.available_numbers

        a_idx, b_idx = self.indexes
        a, b = nums[a_idx], nums[b_idx]

        next_number = self.number_operation.process(a, b)

        news = [n for i, n in enumerate(nums) if i not in (a_idx, b_idx)]
        news.append(next_number)

        return CountdownState(
            AvailableNumbers(tuple(news)),
            state.goal_number,
            f"{self.number_operation.stringify(a, b)} = {next_number}",
            state,
            self
        )
