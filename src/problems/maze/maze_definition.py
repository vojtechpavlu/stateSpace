from abc import ABC, abstractmethod
from typing import Iterable, Union


class Direction:
    """This class represents orthogonal absolute directions.
    This direction also gives a clue about the transition change.
    """

    def __init__(self, name: str, x_diff: int, y_diff: int):
        self.__name = name
        self.__x_diff = x_diff
        self.__y_diff = y_diff

    @property
    def name(self) -> str:
        return self.__name

    @property
    def x_diff(self) -> int:
        """Movement in the x-axis"""
        return self.__x_diff

    @property
    def y_diff(self) -> int:
        """Movement in the y-axis"""
        return self.__y_diff

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, other: "Direction") -> bool:
        return self.x_diff == other.x_diff and self.y_diff == other.y_diff


class Field(ABC):
    """Abstract definition of a field. This field can be either
    wall or a path. Each field also holds it's coordinates.
    """

    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y

    @property
    def x(self) -> int:
        """X-axis coordinate"""
        return self.__x

    @property
    def y(self) -> int:
        """Y-axis coordinate"""
        return self.__y

    @property
    @abstractmethod
    def is_wall(self) -> bool:
        """Returns if the field is wall or not."""

    def __eq__(self, other: "Field") -> bool:
        """Returns if the given object of type Field is the same one."""
        return self.x == other.x and self.y == other.y


class Wall(Field):
    """Field you cannot step on."""

    @property
    def is_wall(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f"Wall([{self.x}, {self.y}])"


class Path(Field):
    """Field you can step on."""

    @property
    def is_wall(self) -> bool:
        return False

    def __repr__(self) -> str:
        return f"Path([{self.x}, {self.y}])"


class Maze:
    """Representation of the maze that is meant to be searched in.
    """

    def __init__(self, fields: Iterable[Field]):
        self.__fields = list(fields)

    @property
    def fields(self) -> tuple[Field]:
        """Tuple of fields this maze is made of."""
        return tuple(self.__fields)

    @property
    def dimensions(self) -> tuple[int, int]:
        """Returns maximum width and maximum height of the maze.
        """
        x_min, x_max, y_min, y_max = self.frame

        return (x_max - x_min + 1), (y_max - y_min + 1)

    @property
    def frame(self) -> tuple[int, int, int, int]:
        """Finds the minimums and maximums coordinates in both x and y axis.
        """

        # Function helpers
        def x(field: Field) -> int:
            """Derive the x-coordinate from the field"""
            return field.x

        def y(field: Field) -> int:
            """Derive the y-coordinate from the field"""
            return field.y

        # Limits of the maze
        x_min, x_max = [min(self.fields, key=x).x, max(self.fields, key=x).x]
        y_min, y_max = [min(self.fields, key=y).y, max(self.fields, key=y).y]

        return x_min, x_max, y_min, y_max

    def field_at(self, x: int, y: int) -> Union[Field, None]:
        """Tries to find a field with given coordinates. When there is no such
        field found, it returns None.
        """
        for field in self.fields:
            if field.x == x and field.y == y:
                return field

    def neighbours(
            self,
            field: Field,
            with_directions: bool = False
    ) -> Union[tuple[Field], tuple[tuple[Direction, Field]]]:
        """Tries to find all the neighbours.

        Based on the `with_directions` flag, it either returns tuples with
        assigned directions or only the neighbours.
        """
        neighbours = []

        # For all the directions
        for direction in directions():

            neighbours.append((
                direction,
                self.neighbour_in_direction(field, direction)
            ))

        # Filter only those non-empty
        neighbours = [n for n in neighbours if n[1]]

        if not with_directions:
            neighbours = [n[1] for n in neighbours]

        return tuple(neighbours)

    def neighbour_in_direction(
            self,
            field: Field,
            direction: Direction
    ) -> Union[Field, None]:
        """Tries to find a neighbour in the given direction from the given
        field. But the given field in direction might not exist in the maze.
        """
        return self.field_at(
            field.x + direction.x_diff,
            field.y + direction.y_diff
        )

    def stringify_maze(
            self,
            fields_to_replace: Iterable[tuple[int, int]] = (),
            replace_char: str = "*"
    ) -> str:
        """Tries to print this maze."""
        x_min, x_max, y_min, y_max = self.frame

        rows = []

        for y in range(y_max, y_min - 1, -1):
            row = []
            for x in range(x_min, x_max + 1):
                field = self.field_at(x, y)
                if (x, y) in fields_to_replace:
                    row.append(replace_char)
                else:
                    row.append("▒" if field.is_wall else " ")
            rows.append(" ".join(row))
        return "\n".join(rows)


_DIRECTIONS = [
    Direction("EAST", 1, 0),
    Direction("NORTH", 0, 1),
    Direction("WEST", -1, 0),
    Direction("SOUTH", 0, -1)
]


def directions() -> tuple["Direction"]:
    """Returns all the available orthogonal directions."""
    return tuple(_DIRECTIONS)
