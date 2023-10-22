from enum import Enum
from typing import Union, Iterable


class Field:
    """A representation of a movable 8-puzzle field.
    On top of its coordinates, it has it's value assigned.
    """

    # Private collection of available values
    __AVAILABLE_VALUES: tuple[str] = tuple([
        '_', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C',
        'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O'
    ])

    def __init__(self, x: int, y: int, value: str):
        self.__x = x
        self.__y = y
        self.__value = value

        if value not in self.available_values():
            raise InconsistentGrid(f"Cannot assign value: '{value}'")

    @property
    def x(self) -> int:
        """X-axis coordinate of the field"""
        return self.__x

    @x.setter
    def x(self, new_x: int):
        """Setter for the x-axis coordinate of the field"""
        self.__x = new_x

    @property
    def y(self) -> int:
        """Y-axis coordinate of the field"""
        return self.__y

    @y.setter
    def y(self, new_y: int):
        """Setter for the y-axis coordinate of the field"""
        self.__y = new_y

    @property
    def value(self) -> str:
        """Value the field is marked with"""
        return self.__value

    @value.setter
    def value(self, new_value: str):
        """Setter for the value of the field. When the value is not in between
        the available values, it raises an error.
        """
        if new_value not in self.available_values():
            raise InconsistentGrid(f"Cannot assign value: '{new_value}'")

        self.__value = new_value

    @property
    def coordinates(self) -> tuple[int, int]:
        """Returns the coordinates as a tuple in format (x, y).
        """
        return self.x, self.y

    @property
    def is_empty(self) -> bool:
        """Returns if the field is empty."""
        return self.value == Field.empty_value()

    @property
    def copy(self) -> "Field":
        """Returns a clone of this field"""
        return Field(self.x, self.y, self.value)

    def __eq__(self, other: "Field") -> bool:
        """Compares two fields based on the `x` and `y` coordinates
        and a value if all these are the same.
        """
        return (
            self.x == other.x and
            self.y == other.y and
            self.value == other.value
        )

    @classmethod
    def available_values(cls) -> tuple[str]:
        """Returns a tuple of the available values to mark the field with.
        """
        return cls.__AVAILABLE_VALUES

    @classmethod
    def empty_value(cls) -> str:
        """Returns the value for an empty field."""
        return cls.__AVAILABLE_VALUES[0]

    def __repr__(self) -> str:
        return f"{[self.value, *self.coordinates]}"


class Move(Enum):
    """Instances of this Enumeration represents the move in a direction
    at the grid board.

    This movement is done switching the empty field to the neighbour in the
    particular direction. The neighbour is being selected by the difference
    of the empty field coordinates (`x_diff` and `y_diff` properties).
    """

    L = (1, 0)
    U = (0, 1)
    R = (-1, 0)
    D = (0, -1)

    def __init__(self, x_diff: int, y_diff: int):
        super().__init__()
        self.__x_diff = x_diff
        self.__y_diff = y_diff

    @property
    def x_diff(self) -> int:
        """Movement in the x-axis coordinate"""
        return self.__x_diff

    @property
    def y_diff(self) -> int:
        """Movement in the y-axis coordinate"""
        return self.__y_diff

    @property
    def diffs(self) -> tuple[int, int]:
        """Composed differences of both x and y axes coordinates into a tuple
        """
        return self.x_diff, self.y_diff

    @property
    def opposite(self) -> "Move":
        """Opposite direction to this one (e.g. opposite of Left is Right)."""
        # Initialize Search map
        opposite_map = {
            Move.L: Move.R,
            Move.U: Move.D,
            Move.R: Move.L,
            Move.D: Move.U,
        }

        # Return the opposite (value for the key)
        return opposite_map[self]

    def neighbour(self, x: int, y: int) -> tuple[int, int]:
        """Find a neighbour coordinates by adding the differences."""
        return x + self.x_diff, y + self.y_diff


class Grid:
    """Instances of this class represent the current board.

    Every board consists of it's fields. These fields are organized into
    a square with side length of multiple fields.

    For this reason, the number of fields has to be equal to this
    `base_size ** 2`. If they are not, the initor raises an error.

    It also has to have an empty field - you wouldn't be able to perform
    any move otherwise. If it's not provided, it raises an error.
    """

    def __init__(self, base_size: int, fields: Iterable[Field]):
        self.__base_size = base_size
        self.__fields = list(fields)

        if len(self.fields) != self.base_size ** 2:
            raise InconsistentGrid("Given grid is not of the given base")

        if not self.empty_field:
            raise InconsistentGrid("Grid doesn't have an empty field")

    @property
    def base_size(self) -> int:
        """Base size of the grid - it represents the width of the board
        square. The number of fields at the board has to be equal to this
        `board_size ** 2`.
        """
        return self.__base_size

    @property
    def fields(self) -> tuple[Field]:
        """All the fields the board consists of"""
        return tuple(self.__fields)

    @property
    def values(self) -> tuple[str]:
        """All the values the board has"""
        return tuple([f.value for f in self.fields])

    @property
    def empty_field(self) -> Field:
        """Tries to find the empty field. When there's no such field found,
        it raises an error.
        """
        for field in self.fields:
            if field.is_empty:
                return field

        # When not found
        raise InconsistentGrid("Grid doesn't have an empty field")

    @property
    def empty_field_coords(self) -> tuple[int, int]:
        """Returns the coordinates of the empty field. When there is no such
        field found, it raises an error.
        """
        empty = self.empty_field
        return empty.x, empty.y

    def possible_movements(
            self,
            include_directions: bool = True
    ) -> Union[tuple[tuple[Move, Field]], tuple[Field]]:
        """Tries to select all the possible moves you can do. These are
        organized into either:

        - tuple of fields (`tuple[Field]`), or
        - tuple of tuples of both move and field (`tuple[tuple[Move, Field]]`)

        this is controlled by the `include_directions`.

        :param include_directions:
            Flag if the output should be just the neighbour fields (`False`)
            or if it should also contain the assigned direction you need to
            perform to get the neighbour field (`True`)
        """
        empty = self.empty_field

        # Initialize possible moves
        dirs: list[Move] = [direction for direction in Move]

        # Find potential neighbour coordinates by mapping each direction
        # to a tuple like (direction, coordinates_in_direction)
        move_coords = [(d, d.neighbour(empty.x, empty.y)) for d in dirs]

        # Map Coordinates to Fields
        move_fields = []

        for move_coord in move_coords:
            # Shorthand coordinates from he second index
            coords = move_coord[1]

            move_fields.append(
                # Append tuple (move_direction, field), while
                # field is mapped from the given coordinates
                (move_coord[0], self.field(coords[0], coords[1]))
            )

        # Filter non-existing fields - when field is not found by coordinates
        # (is None), then skip it. Otherwise, return the original tuple
        neighbours = [mf for mf in move_fields if mf[1] is not None]

        # If should return fields only (filter fields only)
        if not include_directions:
            neighbours = [neigh[1] for neigh in neighbours]

        return tuple(neighbours)

    @property
    def frame(self) -> tuple[int, int, int, int]:
        """Frame of the grid coordinates. This means the minimum and maximum
        coordinate value for both x any y axes.

        Board can technically have minimums as any numbers. Order of these
        values is (x_min, x_max, y_min, y_max).
        """

        # Helper shorthand functions
        def x(field: Field) -> int:
            """Derive the x-axis coordinate from the given field."""
            return field.x

        def y(field: Field) -> int:
            """Derive the y-axis coordinate from the given field."""
            return field.y

        # Take the minimum and maximum coordinates for both axes
        x_min, x_max = min(self.fields, key=x).x, max(self.fields, key=x).x
        y_min, y_max = min(self.fields, key=y).y, max(self.fields, key=y).y

        # Return them as a tuple
        return x_min, x_max, y_min, y_max

    @property
    def height(self) -> int:
        """Height of the board, calculated as a difference between minimum and
        maximum value in the y-axis."""
        return self.frame[3] - self.frame[2] + 1

    @property
    def width(self) -> int:
        """Width of the board, calculated as a difference between minimum and
        maximum value in the x-axis."""
        return self.frame[1] - self.frame[0] + 1

    @property
    def rows(self) -> tuple[tuple[Field]]:
        """Returns the fields of the board organized by rows."""
        rows = []
        for y in range(self.frame[2], self.frame[2] + self.height):
            row = []
            for x in range(self.frame[0], self.frame[0] + self.width):
                row.append(self.field(x, y))
            rows.append(tuple(row))
        return tuple(rows)

    @property
    def column(self) -> tuple[tuple[Field]]:
        """Returns the field of the board organized by columns."""
        columns = []
        for x in range(self.frame[0], self.frame[0] + self.width):
            column = []
            for y in range(self.frame[2], self.frame[2] + self.height):
                column.append(self.field(x, y))
            columns.append(tuple(column))
        return tuple(columns)

    @property
    def copy(self) -> "Grid":
        """Creates a deep copy of this grid."""
        return Grid(self.base_size, tuple([f.copy for f in self.fields]))

    def field(self, x: int, y: int) -> Field:
        """Tries to find a field by the given coordinates. When no such field
        is found, it returns None."""
        for field in self.fields:
            if field.x == x and field.y == y:
                return field

    def switch_fields(self, x1: int, y1: int, x2: int, y2: int) -> "Grid":
        """Tries to switch the fields at given coordinates.

        When there is no field at the any of the two coordinates, it raises
        an error.

        The output is a brand new instance (deep clone) of this grid.
        """
        field1 = self.field(x1, y1)
        field2 = self.field(x2, y2)

        # If any of the fields is missing
        if not field1 or not field2:
            raise CannotSwitch(
                "One of the fields doesn't exist", (x1, y1), (x2, y2))

        # Create deep clone of this grid
        clone = self.copy

        # Switch values between those two fields of the cloned grid
        clone.field(field1.x, field1.y).value = field2.value
        clone.field(field2.x, field2.y).value = field1.value

        return clone

    def move(self, direction: Move) -> "Grid":
        """Tries to move a field on the grid board to the empty one. In other
        words, it switches the two fields, while it tries to find the one that
        when moved in direction, it fills in the empty space leaving the
        previous position empty.

        Simply put: when applied with LEFT direction move, it tries to find
        a neighbour on the right side of the empty field and tries to switch
        those two fields.
        """
        empty = self.empty_field
        movements = self.possible_movements(include_directions=True)
        desired_field: Union[Field, None] = None

        for movement in movements:
            if movement[0] == direction:
                desired_field = movement[1]
                break

        # If any of the fields is not present
        if not desired_field:
            raise CannotSwitch(f"The non-empty field doesn't exist")

        # Try to switch those fields
        return self.switch_fields(
            empty.x,
            empty.y,
            desired_field.x,
            desired_field.y
        )

    def number_of_different_values(self, other: "Grid") -> int:
        """Counts the number of differently placed fields in between the given
        two grids.

        The given grids have to be of a same type:
            - same base size
            - same values
            - same field coordinates

        When any of these conditions is forced, then it raises an error.
        """

        if self.base_size != other.base_size:
            raise IncomparableGrids(
                "Grids have different base size", self, other)

        if sorted(self.values) != sorted(other.values):
            raise IncomparableGrids(
                "Grids have different values", self, other)

        # Differences accumulator
        n_differences = 0

        for field in self.fields:
            other_field = other.field(field.x, field.y)

            # Check existence
            if not other_field:
                raise IncomparableGrids(
                    f"Field '{field}' doesn't exist in the other grid",
                    self,
                    other
                )

            # If the values of the fields are different, add 1, else 0
            n_differences += 1 if field.value != other_field.value else 0

        return n_differences

    @staticmethod
    def of(values: Union[Iterable[str], str], base_size: int = 3) -> "Grid":
        """Tries to create a grid from the given string or an iterable of
        strings.

        The length (number of fields) has to be of the given base squared.
        Otherwise it raises an error.
        """
        values = list(values)

        if len(values) != base_size ** 2:
            raise InconsistentGrid(
                f"Number of values doesn't match the base size: "
                f"{base_size = }, number of fields = {len(values)}")

        fields = []

        for y in range(base_size):
            for x in range(base_size):

                # Deserialization
                row_index = base_size * y
                value = values[row_index + x]

                # Add a brand new field
                fields.append(Field(x, y, value))

        # Return the brand new Grid instance
        return Grid(base_size, fields)

    @staticmethod
    def default_grid_values(base_size: int = 3) -> str:
        """"""
        if base_size == 3:
            return "1234_5678"
        elif base_size == 4:
            return "_123456789ABCDEF"
        elif base_size == 5:
            return "123456789ABC_DEFGHIJKLMNO"

        raise ValueError(f"Not available {base_size = }")


class InconsistentGrid(Exception):
    """This type of error is thrown when the grid is not consistent."""

    def __init__(self, message: str):
        Exception.__init__(self, message)
        self.__message = message

    @property
    def message(self) -> str:
        """Message the error was thrown with (for easier usage)."""
        return self.__message


class IncomparableGrids(Exception):
    """This type of error is raised when the given grids cannot be compared.
    Usually due to the different size or a different set of values used.
    """

    def __init__(self, message: str, g1: Grid, g2: Grid):
        Exception.__init__(self, message)
        self.__message = message
        self.__grids = g1, g2

    @property
    def message(self) -> str:
        """Message the error was thrown with (for easier usage)."""
        return self.__message

    @property
    def grids(self) -> tuple[Grid, Grid]:
        """The two grids not being compatible."""
        return self.__grids


class CannotSwitch(Exception):
    """Error describing the inability to perform a switch of the two fields
    in the grid.
    """

    def __init__(
            self,
            message: str,
            field1_coords: tuple[int, int] = (),
            field2_coords: tuple[int, int] = ()
    ):
        Exception.__init__(self, message)
        self.__message = message
        self.__field1_coords = field1_coords
        self.__field2_coords = field2_coords

    @property
    def message(self) -> str:
        return self.__message

    @property
    def field1_coords(self) -> tuple[int, int]:
        return self.__field1_coords

    @property
    def field2_coords(self) -> tuple[int, int]:
        return self.__field2_coords


