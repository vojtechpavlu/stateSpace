from time import time

from src.fw import State, Operator, StateSpace, Union, algorithms
from src.problems.eight_puzzle.puzzle_definition import Grid, Move
from src.problems.eight_puzzle.puzzle_generator import generate, \
    GeneratorVariant


class GridState(State):
    """"""

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
        """"""
        return self.__grid

    def distance_from(self, state: "GridState") -> float:
        """"""
        return self.grid.number_of_different_values(state.grid)

    def stringify(self) -> str:
        """"""
        lines = []

        for row in self.grid.rows:
            values = [field.value for field in row]
            lines.append(" ".join(values))

        return "\n".join(lines)


class GridOperator(Operator):
    """"""

    def __init__(self, direction_move: Move):
        super().__init__(direction_move.name)
        self.__direction = direction_move

    @property
    def direction(self) -> Move:
        """"""
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


base_size = 3

organized = Grid.default_grid_values(base_size)

initial_grid, goal_grid = generate(
    variant=GeneratorVariant.EASY_9,
    organized=Grid.of(organized, base_size),
    random_steps=20
)

print(initial_grid)

initial_state = GridState(initial_grid)
goal_state = GridState(goal_grid)

operators = [GridOperator(m) for m in Move]

print(initial_state.stringify())
print()
print(goal_state.stringify())

# for algo in ["A_STAR", "GREEDY", "BFS", "DFS"]:
for algo in ["A_STAR", "GREEDY"]:

    print("\n")
    print(100 * "=")

    ss = StateSpace(
        initial_state=initial_state,
        goal_state=goal_state,
        operators=operators,
        algorithm=algo
    )

    print(f"Trying algorithm: '{algo}'")

    start = time()
    solution = ss.solve()
    end = time()

    applied_operators = solution.all_applied_operators()
    print(f"{len(applied_operators)}: {applied_operators}")
    print(f"Solution found in {end - start} seconds")
