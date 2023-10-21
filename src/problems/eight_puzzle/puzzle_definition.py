from enum import Enum


class Field:

    __AVAILABLE_VALUES: tuple[str] = tuple([
        '_', '1', '2', '3', '4', '5', '6', '7',
        '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'
    ])

    def __init__(self, x: int, y: int, value: str):
        self.__x = x
        self.__y = y
        self.__value = value

        if value not in self.available_values():
            raise InconsistentGrid(f"Cannot assign value: '{value}'")

    @property
    def x(self) -> int:
        """"""
        return self.__x

    @x.setter
    def x(self, new_x: int):
        self.__x = new_x

    @property
    def y(self) -> int:
        """"""
        return self.__y

    @y.setter
    def y(self, new_y: int):
        self.__y = new_y

    @property
    def value(self) -> str:
        """"""
        return self.__value

    @value.setter
    def value(self, new_value: str):
        """"""
        if new_value not in self.available_values():
            raise InconsistentGrid(f"Cannot assign value: '{new_value}'")

        self.__value = new_value

    @property
    def is_empty(self) -> bool:
        """"""
        return self.value == Field.empty_value

    @property
    def copy(self) -> "Field":
        """"""
        return Field(self.x, self.y, self.value)

    def __eq__(self, other: "Field") -> bool:
        """Compares two fields based on the `x` and `y` coordinates and a value
        if these are the same. When all matches, they are the same.
        """
        return (
            self.x == other.x and
            self.y == other.y and
            self.value == other.value
        )

    @classmethod
    def available_values(cls) -> tuple[str]:
        return cls.__AVAILABLE_VALUES

    @classmethod
    def empty_value(cls) -> str:
        return cls.__AVAILABLE_VALUES[0]


class Move(Enum):
    """"""

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
        return self.__x_diff

    @property
    def y_diff(self) -> int:
        return self.__y_diff

    @property
    def diffs(self) -> tuple[int, int]:
        return self.x_diff, self.y_diff

    @property
    def opposite(self) -> "Move":
        """"""
        opposite_map = {
            Move.L: Move.R,
            Move.U: Move.D,
            Move.R: Move.L,
            Move.D: Move.U,
        }

        return opposite_map[self]

    def neighbour(self, x: int, y: int) -> tuple[int, int]:
        """"""
        return x + self.x_diff, y + self.y_diff


class Grid:

    def __init__(self, base_size: int, fields: tuple[Field]):
        self.__base_size = base_size
        self.__fields = fields

        if len(fields) != self.base_size ** 2:
            raise InconsistentGrid("Given grid is not of the given base")

        if not self.empty_field:
            raise InconsistentGrid("Grid doesn't have an empty field")

    @property
    def base_size(self) -> int:
        return self.__base_size

    @property
    def fields(self) -> tuple[Field]:
        return self.__fields

    @property
    def empty_field(self) -> Field:
        for field in self.fields:
            if field.is_empty:
                return field
        raise InconsistentGrid("Grid doesn't have an empty field")

    @property
    def empty_field_coords(self) -> tuple[int, int]:
        empty = self.empty_field
        return empty.x, empty.y

    @property
    def possible_movements(
            self,
            include_directions: bool = True
    ) -> tuple[Move, Field]:
        """"""
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
    def copy(self) -> "Grid":
        """"""
        return Grid(self.base_size, tuple([f.copy for f in self.fields]))

    def field(self, x: int, y: int) -> Field:
        """"""
        for field in self.fields:
            if field.x == x and field.y == y:
                return field

    def switch_fields(self, x1: int, y1: int, x2: int, y2: int) -> "Grid":
        """"""
        field1 = self.field(x1, y1)
        field2 = self.field(x2, y2)

        if not field1 or not field2:
            raise CannotSwitch(
                "One of the fields doesn't exist", (x1, y1), (x2, y2))

        # Create deep clone of this grid
        clone = self.copy

        # Switch values between those two fields of the cloned grid
        clone.field(field1.x, field1.y).value = field2.value
        clone.field(field2.x, field2.y).value = field1.value

        return clone


class InconsistentGrid(Exception):

    def __init__(self, message: str):
        Exception.__init__(self, message)
        self.__message = message

    @property
    def message(self) -> str:
        return self.__message


class CannotSwitch(Exception):

    def __init__(
            self,
            message: str,
            field1_coords: tuple[int, int],
            field2_coords: tuple[int, int]
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
