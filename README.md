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
