import random
from enum import Enum

from src.problems.eight_puzzle.puzzle_definition import Grid, Move


def default_initial_grid() -> Grid:
    return Grid.of(values="_12345678", base_size=3)


class GeneratorVariant(Enum):
    """Variant of the puzzle"""

    EASY_8 = ("Easy solution (8 fields)", "_12345678", 3, True)
    EASY_16 = ("Easy solution (16 fields)", "_123456789ABCDEF", 4, True)
    RANDOM_8 = ("Fully randomized (8 fields)", "_12345678", 3, False)
    RANDOM_16 = ("Fully randomized (16 fields)", "_123456789ABCDEF", 4, False)

    def __init__(
            self, description: str, charset: str, base: int, easy: bool
    ):
        """"""
        super().__init__()
        self.__description = description
        self.__charset = charset
        self.__base = base
        self.__easy = easy

    @property
    def description(self) -> str:
        return self.__description

    @property
    def charset(self) -> str:
        return self.__charset

    @property
    def base(self) -> int:
        return self.__base

    @property
    def easy(self) -> bool:
        return self.__easy

    def generate(
            self,
            organized: Grid = default_initial_grid()
    ) -> Grid:
        """"""
        if self.easy:
            current: Grid = organized
            applied = []
            desired_len = 15

            while len(applied) < desired_len:
                possibles = current.possible_movements(include_directions=True)
                selected = random.choice(possibles)
                direction = selected[0]
                applied.append(direction)

                current = current.move(direction)

                applied = prune_operators(applied)

            print(f"Operators: {len(applied)}, {applied}")
            return current
        else:
            charset = list(self.charset)
            random.shuffle(charset)
            return Grid.of(values=''.join(charset), base_size=self.base)


def prune_operators(operators: list[Move]):
    changed = True
    current_operators = operators

    while changed and len(operators) > 2:
        for idx, o in enumerate(current_operators[:-1]):
            if o.opposite == current_operators[idx + 1]:
                current_operators.pop(idx + 1)
                current_operators.pop(idx)
                break
        else:
            changed = False

    return current_operators


def generate(
        variant: GeneratorVariant = GeneratorVariant.EASY_8,
        organized: Grid = default_initial_grid(),
) -> tuple[Grid, Grid]:
    """"""
    return variant.generate(organized=organized), organized
