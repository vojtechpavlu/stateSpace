from src.fw import State, Operator
from src.fw.algorithms.base import Algorithm, NoSolutionFound


class GradientSearch(Algorithm):
    """Search algorithm trying to always minimize the value of a cost function.

    This algorithm chooses each step by its calculated distance from the goal,
    while considering only the closest one (that's where the gradient comes
    to the picture).

    When there's no other step to do that would make the algorithm closer to
    the solution (step to any of children would cause the rise of the cost
    function value) it ends with an error - stuck in a local extrema.
    """

    def __init__(self):
        super().__init__("GRADIENT")

    def next_state(self):
        """Not used in this algorithm."""

    def solve(
            self,
            initial_state: State,
            goal_state: State,
            operators: tuple[Operator]
    ) -> State:
        """"""
        current_state = initial_state
        closed = []

        while current_state != goal_state:
            children: list[State] = []

            # Get the child states
            for operator in operators:
                if operator.can_be_applied(current_state):
                    child = operator.apply(current_state)
                    if child not in closed:
                        children.append(child)

            def evaluate(state: State) -> float:
                """Tries to evaluate the distance between the given state
                and a goal one for easier readability of the code."""
                return state.distance_from(goal_state)

            # Find the child that lowers the cost function the best
            best = min(children, key=evaluate)

            e_curr, e_best = evaluate(current_state), evaluate(best)

            # When the current state is better than the best of its
            # children, the algorithm got into a local extrema and it
            # simply cannot continue in computation
            if e_best > e_curr:
                raise NoSolutionFound(
                    state=current_state,
                    message=f"Stuck at local extrema - none of the children "
                            f"can lower the value of the cost function: "
                            f"{e_curr} < {e_best}"
                )

            # Close the state
            closed.append(current_state)

            # When got better, set the best one as next state
            current_state = best

        # Return the found solution
        return current_state
