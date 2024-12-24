import random
import matplotlib.pyplot as plt
import time
import os
from heapq import heappop, heappush


def create_maze(width, height):
    # Initialize the grid: 1 = wall, 0 = path
    maze = [[1 for _ in range(width)] for _ in range(height)]


    start = (0, 0)
    end = (height - 1, width - 1)

    # Directions for moving in the grid (up, down, left, right)
    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]

    def is_valid(x, y):
        """Check if the cell is valid for carving."""
        return 0 <= x < height and 0 <= y < width and maze[x][y] == 1

    def carve_path_iterative(start_x, start_y):
        """Carve paths iteratively to avoid recursion depth issues and maintain randomness."""
        stack = [(start_x, start_y)]
        while stack:
            x, y = stack[-1]
            maze[x][y] = 0
    

            valid_directions = []
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if is_valid(nx, ny):
                    valid_directions.append((dx, dy))
            random.shuffle(valid_directions)
    
            if valid_directions:
                dx, dy = valid_directions.pop()
                stack.append((x + dx, y + dy))
                maze[x + dx // 2][y + dy // 2] = 0 
            else:
                stack.pop()



    carve_path_iterative(*start)


    maze[start[0]][start[1]] = 0
    maze[end[0]][end[1]] = 0

    return maze

def display_maze(maze):
    plt.figure(figsize=(10, 10))
    plt.imshow(maze, cmap="binary")
    plt.axis("off")
    plt.show()

def a_star(maze, start, end):
    """Perform A* search to find the shortest path in the maze."""
    rows, cols = len(maze), len(maze[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def heuristic(a, b):

        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        _, current = heappop(open_set)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] == 0:
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    heappush(open_set, (f_score[neighbor], neighbor))

    return []

def save_path_as_images(maze, path, start, end, output_folder):
    """Save each step of the pathfinding as an image, including start, end, and heatmap."""
    os.makedirs(output_folder, exist_ok=True)

    heatmap = [[0 for _ in row] for row in maze]
    for step, (x, y) in enumerate(path):
        heatmap[x][y] = step + 1

        maze_copy = [row[:] for row in maze]
        for i, row in enumerate(heatmap):
            for j, value in enumerate(row):
                if value > 0:
                    maze_copy[i][j] = 2

        maze_copy[start[0]][start[1]] = 3
        maze_copy[end[0]][end[1]] = 4

        plt.figure(figsize=(10, 10))
        plt.imshow(maze_copy, cmap="viridis")
        plt.axis("off")
        plt.savefig(os.path.join(output_folder, f"step_{step:03d}.png"))
        plt.close()


def main():
    # Create the maze
    i = 0
    size = 400
    gentime = 0
    trial_count = 100
    while i<trial_count: 
        maze = create_maze(size, size)
    
        # Select two random points that are paths
        while True:
            start = (random.randint(0, size-1), random.randint(0, size-1))
            end = (random.randint(0, size-1), random.randint(0, size-1))
            if maze[start[0]][start[1]] == 0 and maze[end[0]][end[1]] == 0:
                break
    
        # Solve the maze with A*
        start_time = time.time()
        path = a_star(maze, start, end)
        end_time = time.time()
        gentime += end_time-start_time
        i+=1

    print(f"Total time for {trial_count} mazes: {gentime:.5f} seconds")
    gentime = gentime/trial_count
    print(f"Average time taken: {gentime:.5f} seconds")

    with open("time_taken-astar.txt", "w") as file:
        file.write(f"Time taken: {gentime:.6f} seconds\n")


    save_path_as_images(maze, path, start, end, "Astar")

if __name__ == "__main__":
    main()
