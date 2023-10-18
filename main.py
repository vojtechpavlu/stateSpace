from abc import ABC
from typing import Union

from src.fw import algorithms, Operator, StateSpace, State
from src.problems.maze import generate_maze, directions, Maze, Direction, Field

maze_size = 31

# Generate a random Maze
maze = generate_maze(maze_size)

print(maze.stringify_maze())


class Position(State):

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


class DirectionOperator(Operator):

    def __init__(self, direction: Direction):
        super().__init__(direction.name)
        self.direction = direction

    def can_be_applied(self, state: Position) -> bool:
        neighbour = maze.neighbour_in_direction(state.field, self.direction)
        if neighbour:
            return not neighbour.is_wall
        return False

    def apply(self, state: Position) -> Position:
        return Position(
            maze.neighbour_in_direction(state.field, self.direction),
            state,
            self
        )


# Define all the operators
operators = tuple([DirectionOperator(d) for d in directions()])

for algo in algorithms():
    print("\n", 100 * "=")
    print("TRYING ALGORITHM:", algo)
    state_space = StateSpace(
        initial_state=Position(maze.field_at(1, 1)),
        goal_state=Position(maze.field_at(maze_size, maze_size)),
        operators=operators,
        algorithm=algo
    )

    solution = state_space.solve()

    applied_operators = solution.all_applied_operators()
    print(f"{len(applied_operators)}: {applied_operators}")

    parents = solution.all_parents(include_self=True)
    visited = [(p.x, p.y) for p in parents]

    print(maze.stringify_maze(
        fields_to_replace=visited
    ))



