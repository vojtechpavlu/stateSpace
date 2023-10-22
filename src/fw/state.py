from abc import ABC, abstractmethod
from typing import Union


class State(ABC):
    """Abstract base class defining the protocol of a state.

    Initor of this class takes the direct parent of this state and an
    operator applied to it to produce it. Both of these parameters might be
    `None` which implies that this state is origin.
    """

    def __init__(
            self,
            parent: Union["State", None] = None,
            applied_operator: Union["Operator", None] = None
    ):
        self.__parent = parent
        self.__applied_operator = applied_operator

    @property
    def parent(self) -> "State":
        """Direct parent of this state."""
        return self.__parent

    @property
    def applied_operator(self) -> "Operator":
        """Operator applied to the parent to produce this state."""
        return self.__applied_operator

    def all_parents(
            self,
            include_self: bool = False,
            reverse_parents: bool = False
    ) -> tuple["State"]:
        """Returns all the parents of the state in order from the origin
        parent to this state.

        :param include_self: If this state should be included

        :param reverse_parents: If the collection of parents should be reversed
                                (True: this to origin;
                                False: origin to this state)

        :return: A collection of parents in a given order
        """
        all_parents = []

        if include_self:
            all_parents.append(self)

        current_parent = self.parent

        while current_parent:
            all_parents.append(current_parent)
            current_parent = current_parent.parent

        if reverse_parents:
            return tuple(all_parents)
        else:
            return tuple(reversed(all_parents))

    def all_applied_operators(
            self,
            reverse_operators: bool = False
    ) -> tuple["Operator"]:
        """Returns all the operators that has been applied on the way to
        achieve this state in order from the origin state to this one.

        :param reverse_operators: Reversing the order of operators
                                  (True: origin to direct;
                                  False: direct to origin)
        """

        operators = []
        current = self

        while current:
            if current.parent and current.applied_operator:
                operators.append(current.applied_operator)
            current = current.parent

        if reverse_operators:
            return tuple(reversed(operators))
        else:
            return tuple(operators)

    def num_of_parents(self) -> int:
        """Number of parents this state has. This also describes the
        path length."""
        return len(self.all_parents(include_self=False))

    @abstractmethod
    def distance_from(self, state: "State") -> float:
        """Abstract method calculating a distance between this state and
        the given one.

        :param state: State this function calculates the distance from.

        :return: Float representing the distance from the given state.
        """

    def __eq__(self, other: "State") -> bool:
        return self.distance_from(other) == 0


class Operator(ABC):
    """Abstract representation of operation to be performed over a given
    state to transform it to another one.
    """

    def __init__(self, name: str):
        self.__name = name

    @property
    def name(self) -> str:
        """Name of the operator for easier readability."""
        return self.__name

    @abstractmethod
    def can_be_applied(self, state: State) -> bool:
        """Returns if this operator can be applied on a given state."""

    @abstractmethod
    def apply(self, state: State) -> State:
        """Method used to create a new state by application of this operator.
        """

    def __repr__(self):
        return self.name
