from typing import Union

from src.fw import State, Operator
from src.problems.maze import Field, Direction, Maze


class Position(State):
    """This class defines states as 'being at a field'.
    """

    def __init__(
            self,
            field: Field,
            parent: Union["State", None] = None,
            applied_operator: Union["Operator", None] = None
    ):
        super().__init__(parent, applied_operator)
        self.field = field
        self.x = field.x
        self.y = field.y

    def distance_from(self, state: "Position") -> float:
        return (((self.x - state.x) ** 2) + (self.y - state.y) ** 2) ** 0.5

    def __eq__(self, other: "Position"):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"{self.field}"


class DirectionOperator(Operator):
    """This class defines operators as a movement over the maze in a specific
    direction.
    """

    def __init__(self, direction: Direction, maze: Maze):
        super().__init__(direction.name)
        self.__direction = direction
        self.__maze = maze

    @property
    def direction(self) -> Direction:
        return self.__direction

    @property
    def maze(self) -> Maze:
        return self.__maze

    def can_be_applied(self, state: Position) -> bool:
        neighbour = self.maze.neighbour_in_direction(
            state.field, self.direction)

        if neighbour:
            return not neighbour.is_wall

        return False

    def apply(self, state: Position) -> Position:
        return Position(
            self.maze.neighbour_in_direction(state.field, self.direction),
            state,
            self
        )
