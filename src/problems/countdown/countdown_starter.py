from time import time
from typing import Union, Iterable

from src.fw import StateSpace, Algorithm, algorithms
from src.fw.algorithms.base import NoSolutionFound
from src.problems.countdown.countdown_definition import number_operations
from src.problems.countdown.countdown_generator import NumbersType, \
    generate_countdown_board
from src.problems.countdown.countdown_state_space import CountdownOperator, \
    CountdownState


def countdown(
    use_algorithms: Union[Iterable[str], Iterable[Algorithm]] = algorithms(),
    goal_number: Union[int, None] = None,
    numbers_type: Union[NumbersType, None] = None,
    numbers: Union[Iterable[int], None] = None
):
    """
    :param use_algorithms:
        Set of algorithms to be used to solve the problem. When not provided,
        it uses all the defined ones.

    :param goal_number:
        Goal number the algorithm should achieve by applying the mathematical
        operations. When None, it selects it randomly from range [100, 1000].

    :param numbers_type:
        Type of numbers generator. Either this parameter or the `numbers` has
        to be provided, otherwise it raises an error.

    :param numbers:
        An iterable of integers predefining the set of numbers to be played
        with. Either this parameter or the `numbers_type` has to be provided,
        otherwise it raises an error.
    """
    available_numbers, goal_number = generate_countdown_board(
        goal_number=goal_number,
        numbers_type=numbers_type,
        numbers=numbers
    )

    operators = []

    for operation in number_operations():
        for l_idx, lower_idx in enumerate(available_numbers.numbers):
            for u_idx, upper_idx in enumerate(available_numbers.numbers):
                if l_idx != u_idx:
                    operators.append(
                        CountdownOperator(operation, l_idx, u_idx))

    initial = CountdownState(available_numbers, goal_number)
    goal = CountdownState(available_numbers, goal_number)

    print("Given Numbers:", available_numbers)
    print("Goal:", goal_number)

    for algo in use_algorithms:
        print(50 * "=", "\n")

        ss = StateSpace(
            initial_state=initial,
            goal_state=goal,
            operators=operators,
            algorithm=algo
        )

        print(f"Trying algorithm: {algo}")

        try:
            start = time()
            solution = ss.solve()
            end = time()
            applied_operators = solution.stringified_path[1:]
            print(f"{len(applied_operators)}: {applied_operators}")
            print(f"Solution found in {end - start} seconds")

        except NoSolutionFound as err:
            print(err.message)




