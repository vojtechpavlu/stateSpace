import time
from typing import Iterable, Union

from src.fw import Algorithm, StateSpace, algorithms
from src.fw.algorithms.base import NoSolutionFound
from src.problems.maze import generate_maze, directions, Maze
from src.problems.maze.maze_state_space import Position, DirectionOperator


def start_maze_solving(
    maze_size: int = 0,
    maze: Union[Maze, None] = None,
    use_algorithms: Union[Iterable[Algorithm], Iterable[str]] = algorithms(),
    print_time: bool = True,
    print_empty: bool = True,
    print_path: bool = True,
    print_error_path: bool = True,
    print_operators: bool = True,
    print_number_of_operators: bool = True
):
    """Facade function to schedule solution of a random maze.

    For each of the algorithm, it tries to solve the maze.

    :param maze_size:
        Size of the inner maze fields (assuming a square-shaped maze).
        Either this parameter has to be given or the `maze` one.

    :param maze:
        Maze to be used. Either this parameter has to be given or the
        `maze_size` to new to be generated.

    :param use_algorithms:
        An iterable collection of algorithms to be used to solve the maze.
        By default, it takes all the implemented ones.

    :param print_time:
        Flag if the times of solving should be printed.

    :param print_empty:
        Flag if the empty maze (without any path) to be solved should be
        printed in the first place.

    :param print_path:
        Flag if the found path through the maze should be shown.

    :param print_error_path:
        Flag if the erroneous path through the maze should be shown.

    :param print_operators:
        Flag if the list of applied operators on the path should be printed.

    :param print_number_of_operators:
        Flag if the number of operators applied on the path should be printed.
    """

    # Generate empty maze if not given one
    maze = maze if maze else generate_maze(maze_size)

    # If print empty maze
    if print_empty:
        print(maze.stringify_maze())

    # Prepare operators
    operators = tuple([DirectionOperator(d, maze) for d in directions()])

    # For each of the given algorithms
    for algorithm in use_algorithms:
        print(80 * "=")
        print(f"Finding solution with '{algorithm}' algorithm")

        # Define State Space
        state_space = StateSpace(
            initial_state=Position(maze.field_at(1, 1)),
            goal_state=Position(maze.field_at(maze_size, maze_size)),
            operators=operators,
            algorithm=algorithm
        )

        try:
            started = time.time()
            solution = state_space.solve()
            ended = time.time()

            # Analyze applied operators
            applied_operators = solution.all_applied_operators()

            if print_time:
                print(f"Solution found in {ended - started} seconds")

            if print_number_of_operators:
                print(f"Number of operators applied: {len(applied_operators)}")

            if print_operators:
                print(f"Operators: {applied_operators}")

            if print_path:
                parents = solution.all_parents(include_self=True)
                visited = [(parent.x, parent.y) for parent in parents]
                print(maze.stringify_maze(fields_to_replace=visited))

        except NoSolutionFound as error:
            print(error.message)
            if print_error_path:
                parents = error.state.all_parents(include_self=True)
                visited = [(parent.x, parent.y) for parent in parents]
                print(maze.stringify_maze(fields_to_replace=visited))

        print("\n")
