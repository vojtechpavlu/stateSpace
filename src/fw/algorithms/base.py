from abc import ABC, abstractmethod

from src.fw import State, Operator, Union


class Algorithm(ABC):
    """Abstract class declaring the protocol of an algorithm to search the
    state space.
    """

    def __init__(self, name: str):
        self.__name = name
        self.__goal: Union[State, None] = None

        # Scheduled states to be searched in
        self.__fringe: list[State] = []

        # States the algorithm already searched and found their descendants
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

    def drop_from_fringe(self, state: State):
        self.__fringe.remove(state)

    def add_to_closed(self, state: State):
        self.__closed.append(state)

    def is_in_closed(self, state: State) -> bool:
        return state in self.closed

    @property
    def name(self) -> str:
        """Name of the algorithm"""
        return self.__name

    @property
    def goal_state(self) -> State:
        """State the algorithm should be trying to reach."""
        return self.__goal

    @goal_state.setter
    def goal_state(self, goal: State):
        """Setter for the goal state the algorithm should be trying to reach.
        """
        self.__goal = goal

    @abstractmethod
    def next_state(self):
        """Provides next state to be searched."""

    def solve(
            self,
            initial_state: State,
            goal_state: State,
            operators: tuple[Operator]
    ) -> State:
        """Tries to find the solution.
        When finished, it returns the state equivalent to the goal one with
        assigned tree-path from the root with all the applied operators.
        """
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

    def __repr__(self):
        return self.name


class NoSolutionFound(Exception):
    """Exception risen in case the algorithm reached a specific limit or the
    solution is not available for the algorithm in any other way.
    """
