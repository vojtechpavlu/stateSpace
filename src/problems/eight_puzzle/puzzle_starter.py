from time import time
from typing import Union, Iterable

from src.fw import Algorithm, algorithms, StateSpace
from src.problems.eight_puzzle.puzzle_definition import Grid, Move
from src.problems.eight_puzzle.puzzle_generator import generate, \
    GeneratorVariant
from src.problems.eight_puzzle.puzzle_state_space import GridState, \
    GridOperator


def start_8_puzzle(
        steps: int,
        easy: bool = True,
        base_size: int = 3,
        algos: Union[Iterable[Algorithm], Iterable[str]] = algorithms()
):

    # Get the organized grid
    organized = Grid.default_grid_values(base_size)

    # Shuffle it up
    initial_grid, goal_grid = generate(
        variant=GeneratorVariant.find(base_size, easy),
        organized=Grid.of(organized, base_size),
        random_steps=steps
    )

    # Create the states of them
    initial_state = GridState(initial_grid)
    goal_state = GridState(goal_grid)

    # Prepare the operators
    operators = [GridOperator(m) for m in Move]

    # Print the initial and the goal states
    print(initial_state.stringify())
    print()
    print(goal_state.stringify())

    for algo in algos:
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
