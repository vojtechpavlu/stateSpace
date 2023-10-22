import random
from enum import Enum

from src.problems.eight_puzzle.puzzle_definition import Grid, Move


class GeneratorVariant(Enum):
    """Variant of the puzzle generator.

    There are two major groups for such ways of generating:

        - EASY - method of randomly applying the movements of the empty field.
                 This produces perfectly consistent and solvable puzzle. This
                 approach is highly recommended for its guarantees and ability
                 to parametrize the randomization (maximum number of steps).
                 The drawback is that it doesn't guarantees the minimal number
                 of steps needed to find a solution. There's only a simple
                 mechanism to prevent the "getting back" implemented. Could
                 be solved by using another State Space tracking the visited
                 grids states and applied operators.

        - RANDOM - method of shuffling all the values randomly; in some
                   circumstances it might produce a puzzle with no existing
                   solution. On the other hand, its very effective method to
                   create hard method with very limited resources and time.
    """

    EASY_9 = (
        "Easy solution (8 fields)", Grid.default_grid_values(3), 3, True)

    EASY_16 = (
        "Easy solution (16 fields)", Grid.default_grid_values(4), 4, True)

    EASY_25 = (
        "Easy solution (25 fields)", Grid.default_grid_values(5), 5, True)

    RANDOM_9 = (
        "Fully randomized (8 fields)", Grid.default_grid_values(3), 3, False)

    RANDOM_16 = (
        "Fully randomized (16 fields)", Grid.default_grid_values(4), 4, False)

    RANDOM_25 = (
        "Fully randomized (25 fields)", Grid.default_grid_values(5), 5, False)

    def __init__(
            self, description: str, charset: str, base: int, easy: bool
    ):
        super().__init__()
        self.__description = description
        self.__charset = charset
        self.__base = base
        self.__easy = easy

    @property
    def description(self) -> str:
        """Description of a randomization mechanism"""
        return self.__description

    @property
    def charset(self) -> str:
        """Values the grid should be based on"""
        return self.__charset

    @property
    def base(self) -> int:
        """Base size of the grid (number of fields at the side of the grid)."""
        return self.__base

    @property
    def easy(self) -> bool:
        """If the mechanism provides an easy puzzle or a hard one."""
        return self.__easy

    def generate(
            self,
            organized: Grid,
            random_steps: int = 12
    ) -> Grid:
        """Tries to generate a randomized grid."""
        if self.easy:
            current: Grid = organized
            applied = []

            while len(applied) < random_steps:
                possibles = current.possible_movements(include_directions=True)
                selected = random.choice(possibles)
                direction = selected[0]
                applied.append(direction)

                current = current.move(direction)

                applied = prune_operators(applied)

            operator_names = [o.name for o in applied]
            print(f"Operators: {len(operator_names)}, {operator_names}")
            return current
        else:
            charset = list(self.charset)
            random.shuffle(charset)
            return Grid.of(values=''.join(charset), base_size=self.base)


def prune_operators(operators: list[Move]):
    """Tries to remove the consecutive opposite operators from the generation
    mechanism. These opposites cause that you easily return to the previously
    found state - it generates redundancy due to the non-systematic manner of
    random steps generating.

    This function is used to minimize the difference between requested number
    of steps needed to solve the problem (minimum) and the maximum
    randomization steps.
    """
    changed = True
    current_operators = operators

    while changed and len(operators) >= 2:
        for idx, o in enumerate(current_operators[:-1]):
            if o.opposite == current_operators[idx + 1]:
                current_operators.pop(idx + 1)
                current_operators.pop(idx)
                break
        else:
            changed = False

    return current_operators


def generate(
        variant: GeneratorVariant = GeneratorVariant.EASY_9,
        organized: Grid = Grid.of(Grid.default_grid_values(), 3),
        random_steps: int = 12
) -> tuple[Grid, Grid]:
    """This function generates the whole grid."""
    return (
        variant.generate(
            organized=organized,
            random_steps=random_steps
        ),
        organized
    )
