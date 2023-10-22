"""This package contains a definition of the 8 Puzzle problem with its commonly
known variations."""

from .puzzle_starter import start_8_puzzle
from .puzzle_generator import GeneratorVariant
from .puzzle_state_space import GridState, GridOperator
from .puzzle_definition import (
    Move, Field, Grid, InconsistentGrid, IncomparableGrids, CannotSwitch
)
