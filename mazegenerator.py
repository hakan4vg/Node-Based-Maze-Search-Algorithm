import random
import matplotlib.pyplot as plt

def create_maze(width, height):
    # Initialize the grid: 1 = wall, 0 = path
    maze = [[1 for _ in range(width)] for _ in range(height)]

    # Start and end points
    start = (0, 0)
    end = (height - 1, width - 1)

    # Directions for moving in the grid (up, down, left, right)
    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]

    def is_valid(x, y):
        """Check if the cell is valid for carving."""
        return 0 <= x < height and 0 <= y < width and maze[x][y] == 1

    def carve_path(x, y):
        """Carve paths recursively using DFS."""
        maze[x][y] = 0  # Mark as a path
        random.shuffle(directions)  # Randomize the order of exploration

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                # Carve a corridor between (x, y) and (nx, ny)
                maze[x + dx // 2][y + dy // 2] = 0
                carve_path(nx, ny)

    # Carve the maze starting from the top-left corner
    carve_path(*start)

    # Ensure the start and end points are paths
    maze[start[0]][start[1]] = 0
    maze[end[0]][end[1]] = 0

    return maze

def display_maze(maze):
    """Display the maze using matplotlib."""
    plt.figure(figsize=(10, 10))
    plt.imshow(maze, cmap="binary")
    plt.axis("off")
    plt.show()

# Create and display a 200x200 maze
maze = create_maze(200, 200)
display_maze(maze)
