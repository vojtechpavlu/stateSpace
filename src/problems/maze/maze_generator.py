import random

from src.problems.maze import Maze, Path, Wall


def generate_maze(base: int) -> Maze:
    """Generates a random maze from the given base size. These mazes might have
    multiple ways to get to the goal. It also guarantees that every field
    with both coordinates being odd, it points to a path (e.g. [1, 1]).

    When the given base size is even or lower than 5, it rises an error.
    """

    if base % 2 == 0:
        raise ValueError(f"Cannot create a maze of an even number: {base}")
    elif base < 5:
        raise ValueError(f"Given base number is too small: {base}")

    # Initialize the maze made of walls only
    proto_fields = [[0 for _ in range(base)] for _ in range(base)]

    base_fields = []

    for ridx, row in enumerate(proto_fields):
        for fidx, field in enumerate(row):
            if ridx % 2 == 1 and fidx % 2 == 1:
                base_fields.append((ridx, fidx))
                proto_fields[ridx][fidx] = 1

    directions = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1)
    ]

    for base_field in base_fields:
        direction = random.choice(directions)
        x, y = base_field
        new_x, new_y = x + direction[0], y + direction[1]
        proto_fields[new_y][new_x] = 1

    # Add a top line of walls
    proto_fields.insert(0, [1 for _ in range(base)])

    # Add a bottom line of walls
    proto_fields.append([1 for _ in range(base)])

    # Add side walls
    for row in proto_fields:
        row.insert(0, 1)
        row.append(1)

    fields = []

    for row_idx, row in enumerate(proto_fields):
        for field_idx, field in enumerate(row):
            is_wall = proto_fields[row_idx][field_idx] == 1
            x, y = field_idx, row_idx
            fields.append(Wall(x, y) if is_wall else Path(x, y))

    return Maze(fields)
