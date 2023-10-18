from abc import ABC, abstractmethod

from src.fw import State, Operator


class Algorithm(ABC):
    """"""

    def __init__(self, name: str):
        """"""
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    @abstractmethod
    def next_state(self):
        """"""

    @abstractmethod
    def solve(
            self,
            initial_state: State,
            goal_state: State,
            operators: tuple[Operator]
    ) -> State:
        """"""

    def __repr__(self):
        return self.name


class BlindAlgorithm(Algorithm, ABC):
    """Base for blind algorithm that defines the general algorithm.
    The only method that has to be overridden is the `next_state`.
    """

    def __init__(self, name: str):
        super().__init__(name)
        self.__fringe: list[State] = []
        self.__closed: list[State] = []

    @property
    def fringe(self) -> tuple[State]:
        return tuple(self.__fringe)

    @property
    def closed(self) -> tuple[State]:
        return tuple(self.__closed)

    def add_to_fringe(self, state: State):
        self.__fringe.append(state)

    def pop_from_fringe(self, index: int) -> State:
        return self.__fringe.pop(index)

    def add_to_closed(self, state: State):
        self.__closed.append(state)

    def is_in_closed(self, state: State) -> bool:
        return state in self.closed

    def solve(
            self,
            initial_state: State,
            goal_state: State,
            operators: tuple[Operator]
    ) -> State:
        self.add_to_fringe(initial_state)

        while len(self.fringe) > 0:
            current = self.next_state()

            # When the current state is the desired one
            if current == goal_state:
                return current

            # When the current state was already closed
            if self.is_in_closed(current):
                continue

            # Try all the operators
            for operator in operators:

                # If can this operator be applied on a current state
                if operator.can_be_applied(current):

                    # Schedule further searching of the descendant
                    self.add_to_fringe(operator.apply(current))

            # Close after searching
            self.add_to_closed(current)

        # There's no state to be searched in and still no solution found
        raise NoSolutionFound()


class NoSolutionFound(Exception):
    """"""
