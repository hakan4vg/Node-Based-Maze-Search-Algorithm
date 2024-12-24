import random
import matplotlib.pyplot as plt
import time
import os
from heapq import heappop, heappush

def create_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]
    start = (0, 0)
    end = (height - 1, width - 1)
    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]

    def is_valid(x, y):
        return 0 <= x < height and 0 <= y < width and maze[x][y] == 1

    def carve_path_iterative(start_x, start_y):
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

def find_router_nodes(maze):
    rows, cols = len(maze), len(maze[0])
    router_nodes = []
    
    for x in range(rows):
        for y in range(cols):
            if maze[x][y] == 0:
                neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                           if 0 <= x + dx < rows and 0 <= y + dy < cols and maze[x + dx][y + dy] == 0]
                if len(neighbors) > 2:
                    router_nodes.append((x, y))
    
    return router_nodes

def find_neighbors(current_node, maze):
    rows, cols = len(maze), len(maze[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    neighbors = []
    x, y = current_node

    for dx, dy in directions:
        temp_x, temp_y = x + dx, y + dy
        path = []
        
        while 0 <= temp_x < rows and 0 <= temp_y < cols and maze[temp_x][temp_y] == 0:
            path.append((temp_x, temp_y))
            neighbor_count = sum(1 for d in directions 
                               if 0 <= temp_x + d[0] < rows and 0 <= temp_y + d[1] < cols 
                               and maze[temp_x + d[0]][temp_y + d[1]] == 0)
            
            if neighbor_count > 2 and (temp_x, temp_y) != current_node:
                neighbors.append(((temp_x, temp_y), path))
                break
                
            temp_x += dx
            temp_y += dy

    return neighbors

def a_star(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        current = heappop(open_set)[1]

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] == 0:
                tentative_g = g_score[current] + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, end)
                    f_score[neighbor] = f
                    heappush(open_set, (f, neighbor))

    return None

def optimize_path(maze, start, end):
    router_nodes = find_router_nodes(maze)
    router_nodes.append(start)
    router_nodes.append(end)
    
    current = start
    final_path = []
    visited = {start}
    
    while current != end:
        neighbors = find_neighbors(current, maze)
        if not neighbors:
            break
            
        next_node = None
        min_distance = float('inf')
        best_path = None
        
        for neighbor, path in neighbors:
            if neighbor not in visited:
                distance = len(path) + abs(neighbor[0] - end[0]) + abs(neighbor[1] - end[1])
                if distance < min_distance:
                    min_distance = distance
                    next_node = neighbor
                    best_path = path
        
        if next_node is None:
            break
            
        final_path.extend(best_path)
        current = next_node
        visited.add(current)
    
    if current != end:
        direct_path = a_star(maze, current, end)
        if direct_path:
            final_path.extend(direct_path)
    
    return final_path

def save_path_as_images_hakan(maze, path, output_folder, start, end):
    os.makedirs(output_folder, exist_ok=True)
    maze_state = [row[:] for row in maze]
    step = 0
    router_nodes = find_router_nodes(maze)
    

    maze_state[start[0]][start[1]] = 6
    maze_state[end[0]][end[1]] = 7
    
    path_intersections = []
    for point in path:
        if point in router_nodes or point == start or point == end:
            path_intersections.append(point)
    
    for i in range(len(path_intersections) - 1):
        current = path_intersections[i]
        next_node = path_intersections[i + 1]
        
        sub_path = []
        current_index = path.index(current)
        next_index = path.index(next_node)
        sub_path = path[current_index:next_index + 1]
        

        maze_state[current[0]][current[1]] = 3
        plt.figure(figsize=(10, 10))
        plt.imshow(maze_state, cmap="viridis")
        plt.axis("off")
        plt.savefig(os.path.join(output_folder, f"step_{step:03d}_a.png"))
        plt.close()
        

        maze_state[next_node[0]][next_node[1]] = 4
        plt.figure(figsize=(10, 10))
        plt.imshow(maze_state, cmap="viridis")
        plt.axis("off")
        plt.savefig(os.path.join(output_folder, f"step_{step:03d}_b.png"))
        plt.close()
        

        for x, y in sub_path:
            if (x, y) != current and (x, y) != next_node and (x, y) != start and (x, y) != end:
                maze_state[x][y] = 2
        plt.figure(figsize=(10, 10))
        plt.imshow(maze_state, cmap="viridis")
        plt.axis("off")
        plt.savefig(os.path.join(output_folder, f"step_{step:03d}_c.png"))
        plt.close()
        

        for x, y in sub_path:
            if (x, y) != current and (x, y) != next_node and (x, y) != start and (x, y) != end:
                maze_state[x][y] = 5
        plt.figure(figsize=(10, 10))
        plt.imshow(maze_state, cmap="viridis")
        plt.axis("off")
        plt.savefig(os.path.join(output_folder, f"step_{step:03d}_d.png"))
        plt.close()
        
        step += 1
    
    plt.figure(figsize=(10, 10))
    plt.imshow(maze_state, cmap="viridis")
    plt.axis("off")
    plt.savefig(os.path.join(output_folder, "final.png"))
    plt.close()

def main():
    size = 400
    
    gentime = 0
    i = 0
    trial_count = 100
    while i<trial_count: 
        maze = create_maze(size, size)
        
        
        while True:
            start = (random.randint(0, size-1), random.randint(0, size-1))
            end = (random.randint(0, size-1), random.randint(0, size-1))
            if maze[start[0]][start[1]] == 0 and maze[end[0]][end[1]] == 0:
                break
        
        start_time = time.time()
        optimized_path = optimize_path(maze, start, end)
        end_time = time.time()
        gentime += end_time-start_time
        i+=1
    print(f"Total time for {trial_count} mazes: {gentime:.5f} seconds")
    gentime = gentime/trial_count
    print(f"Average time taken: {gentime:.5f} seconds")
    
    with open("time_taken_nodebased.txt", "w") as file:
        file.write(f"Time taken: {gentime:.6f} seconds\n")
    save_path_as_images_hakan(maze, optimized_path, "nodeBased", start, end)

if __name__ == "__main__":
    main()