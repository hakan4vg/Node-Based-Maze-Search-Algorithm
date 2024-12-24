# Node-Based Maze Search Algorithm

This project implements a node-based maze search algorithm using Python. It includes the generation of mazes and finding the shortest path using the A* algorithm. The project also visualizes the maze and the pathfinding process.


### Files

- **mazegenerator.py**: Contains the implementation of a maze generator using Depth-First Search (DFS).

- **Astar.py**: Contains the implementation of the A* algorithm for pathfinding in a maze.

- **Nodebased.py**: Contains the implementation of a node-based maze search algorithm which iterates among the cells to create a mapping of intersections and their neighbouring intersections similar to network routing. Instead of using A* at a cell based environment, this tries to calculate the shortest path with A* among the intersection nodes.
