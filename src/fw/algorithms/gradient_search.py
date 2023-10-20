from typing import Union

from src.fw import State, Operator
from src.fw.algorithms.base import Algorithm, NoSolutionFound


class GradientSearch(Algorithm):
    """"""

    def __init__(self):
        super().__init__("GRADIENT")

    def next_state(self):
        """"""

    def solve(
            self,
            initial_state: State,
            goal_state: State,
            operators: tuple[Operator]
    ) -> State:
        """"""
        current_state = initial_state

        while current_state != goal_state:
            children: list[State] = []

            # Get the child states
            for operator in operators:
                if operator.can_be_applied(current_state):
                    children.append(operator.apply(current_state))

            def helper_function(state: State) -> float:
                """Tries to evaluate the distance between the given state
                and a goal one for easier readability of the code."""
                return state.distance_from(goal_state)

            # Find the child that lowers the cost function the best
            best = min(children, key=helper_function)

            # When the current state is better than the best of its
            # children, the algorithm got into a local extrema and it
            # simply cannot continue in computation
            if helper_function(best) > helper_function(current_state):
                raise NoSolutionFound(
                    state=current_state,
                    message=("Stuck at local extrema - none of the children "
                             "can lower the value of the cost function")
                )

            # When got better, set the best one as next state
            current_state = best

        # Return the found solution
        return current_state
