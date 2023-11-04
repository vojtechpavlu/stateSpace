"""This problem is a naive implementation of a domain inspired by a famous
british television game show Countdown (more specifically the 'Numbers round').

The goal of this game is to find a path of basic mathematical operations
applied on given numbers to reach the given goal number.

For reference, have a look in these links:
    - https://en.wikipedia.org/wiki/Countdown_(game_show)#Numbers_Round
    - https://www.youtube.com/watch?v=JTtu_O3E41U
"""

from .countdown_generator import NumbersType
from .countdown_starter import countdown
