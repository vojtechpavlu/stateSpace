# State Space Framework

This simple project is meant to be used as a educational tool to support 
the teaching of Symbolic methods of Artificial Intelligence at
[Smíchovská střední průmyslová škola a gymnázium](https://ssps.cz/).


## Project Structure

This project contains all the source codes in the `src` package. In there, you
can find two submodules:

- `fw` - whole [State Space framework](#framework) with all means
- `problems` - definition of [example problems](#problems) the State Space 
  approach can be useful for
  
---

## Framework

The whole framework is based on an [State Space abstraction](#state-space-abstraction)
and naive [algorithm implementations](#implemented-algorithms) for finding paths in graphs.


### State Space Abstraction

State Space can be considered as a mechanism for transforming a given problem 
into an oriented graph with multiple nodes (representing individual states),
where you can move between.

The actual transition from one state to another is performed using something 
called Operator.

The expected solution of such a graph-based problem is an implicit path through
the given space - a list of steps you have to do to get from the initial state
to the goal one. In another words, a list of operators you have to apply for
the transition from the initial position to the desired goal.


### Implemented Algorithms

Currently, you can find a few naive implementations of algorithms used for such
a search:

- **Non-informed Search**
    - Depth-First Search
    - Breadth-First Search

- **Heuristic Search**
    - Greedy Search
    - A*
    - Gradient Search
    
- **Random Search**
    - Fully Random Search

---

## Problems

Here's a list of implemented example problems the State Space can be useful
for.

### Path Searching in Maze

The goal of this problem is simple - to find a path from the start to the end.

The actual maze could be imagined as following:

```
▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒
▒       ▒       ▒
▒ ▒ ▒   ▒   ▒   ▒
▒           ▒   ▒
▒   ▒ ▒ ▒ ▒ ▒   ▒
▒   ▒   ▒       ▒
▒   ▒   ▒   ▒ ▒ ▒
▒               ▒
▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒
```

The start is (by default) defined at position `[0, 0]`, which is at the bottom
left corner, while the end is assumed to be at the opposite corner (top right).

The path can be described as at the following figure:

```
▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒
▒       ▒     * ▒
▒ ▒ ▒   ▒   ▒ * ▒
▒           ▒ * ▒
▒   ▒ ▒ ▒ ▒ ▒ * ▒
▒   ▒   ▒ * * * ▒
▒   ▒   ▒ * ▒ ▒ ▒
▒ * * * * *     ▒
▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒
```

To enable the search algorithms, you can trigger it by the following snippet
in the `main.py` file:

````python
from src.problems.maze.maze_starter import start_maze_solving

start_maze_solving(
    maze_size=21,
    use_algorithms=["GRADIENT", "GREEDY", "A_STAR", "BFS", "DFS"]
)
````


### 8-Puzzle

8-Puzzle is a simple board-based game where you are ordering a grid of tiles
(fields) with assigned values. It's called 8-Puzzle because there are 8 of
these fields you can move in the 9 space grid. There are also variants with
larger number of squares you can move around but with only single empty one.

The grid might look like something like this:

```
1 5 2 3
8 _ 4 7
9 D 6 B
C E A F
```

with a goal (ordered grid) specified as:

```
_ 1 2 3
4 5 6 7
8 9 A B
C D E F
```

To define such a task, you can simply start the generation mechanism and actual
test by the following code from `main.py`:


```python
from src.problems.eight_puzzle import start_8_puzzle

start_8_puzzle(
    steps=10,
    base_size=4,
    algos=["GRADIENT", "GREEDY", "A_STAR", "BFS"]
)
```
