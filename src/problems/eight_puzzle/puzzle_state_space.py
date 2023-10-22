from typing import Union

from src.fw import State, Operator
from .puzzle_definition import Grid, Move


class GridState(State):
    """State represented as a current Grid with fields positioned."""

    def __init__(
            self,
            grid: Grid,
            parent: Union["GridState", None] = None,
            applied_operator: Union["GridOperator", None] = None
    ):
        super().__init__(parent, applied_operator)
        self.__grid = grid

    @property
    def grid(self) -> Grid:
        """The actual grid"""
        return self.__grid

    def distance_from(self, state: "GridState") -> float:
        """Calculates the distance between misplaced fields using manhattan
        distance."""
        return self.grid.manhattan_distance(state.grid)

    def stringify(self) -> str:
        """Tries to stringify the grid"""
        lines = []

        for row in self.grid.rows:
            values = [field.value for field in row]
            lines.append(" ".join(values))

        return "\n".join(lines)


class GridOperator(Operator):
    """Operator represented as a move in direction."""

    def __init__(self, direction_move: Move):
        super().__init__(direction_move.name)
        self.__direction = direction_move

    @property
    def direction(self) -> Move:
        """Direction it can move to."""
        return self.__direction

    def can_be_applied(self, state: GridState) -> bool:
        possibles = state.grid.possible_movements(include_directions=True)
        directions = [possible[0] for possible in possibles]
        return self.direction in directions

    def apply(self, state: GridState) -> GridState:
        new_grid = state.grid.move(self.direction)

        return GridState(
            grid=new_grid,
            parent=state,
            applied_operator=self
        )
