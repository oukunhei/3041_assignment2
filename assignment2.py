# use Euclidean distance as heuristic function
import sys
import heapq
import queue
from typing import List, Dict, Tuple
from pathlib import Path
import time
import argparse
from collections import deque
import math

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# bfs algorithm steps：
# 1 initialize the queue (add start node), use dqueue for better performance
# 2 pop an element from head 
# 3 decide if it is the end point, if yes then find its path in visited 
# 4 if not end node then add its neighbors to the queue
# if no path, end when there's no element in the queue
def get_neighbors(pos: Tuple[int, int], maze: List[List[str]], rows: int, cols: int) -> List[Tuple[int, int]]:
    neighbors = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # 右、左、下、上
    for dx, dy in directions:
        new_x, new_y = pos[0] + dx, pos[1] + dy
        if 0 <= new_x < rows and 0 <= new_y < cols and maze[new_x][new_y] != '#':
            neighbors.append((new_x, new_y))
    return neighbors

def BFS(maze: List[List[str]], start: Tuple[int, int], end: Tuple[int, int], rows: int, cols: int):
    path_exist=False
    q = deque()
    q.append(start)
    parent = {start: None}
    visited = set()
    visited.add(start)
    start_time = time.perf_counter()

    while q:
        current = q.popleft()
        if current == end:
            path_exist = True
            break

        for neighbor in get_neighbors(current, maze, rows, cols):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                q.append(neighbor)

    end_time = time.perf_counter()
    elapsed_time = round((end_time - start_time) * 1000, 4)

    if path_exist:
        length = 0
        while current is not None:
            current = parent[current]
            length += 1
        length -= 1  # minus the start node
    else:
        length = -1 # no path

    expanded_states = len(visited)

    return {"algorithm": "BFS", "path_exist": path_exist, "length": length, "expanded_states": expanded_states, "elapsed_time": elapsed_time}


# A* algorithm
# 1 initialize heap (g，node) 
# 2 get an element from the heap (the one with smallest f)
# 3 if end, find its path in CLOSED
# 4 if not end, add its neighbors to the heap with f=g+h
def a_star_0(maze: List[List[str]], start: Tuple[int, int], end: Tuple[int, int], rows: int, cols: int):
    path_exist = False
    OPEN = []
    heapq.heappush(OPEN, (0, start)) # since h=0, we have f = g
    CLOSED = {start: 0} # store g value for each node in CLOSED
    start_time = time.perf_counter()

    while OPEN:
        g, current = heapq.heappop(OPEN)
        if current == end:
            path_exist = True
            break

        for neighbor in get_neighbors(current, maze, rows, cols):
            if neighbor not in CLOSED:
                CLOSED[neighbor] = g + 1
                heapq.heappush(OPEN, (g + 1, neighbor)) 
            # we don't need to update g for nodes in CLOSED since every step is 1
            # we won't find a shorter path to a node in CLOSED after we add it to CLOSED
    end_time = time.perf_counter()
    elapsed_time = round((end_time - start_time) * 1000, 4)
    if path_exist:
        length = CLOSED[end]
    else:
        length = -1
    expanded_states = len(CLOSED)
    return {"algorithm": "A* (h=0)", "path_exist": path_exist, "length": length, "expanded_states": expanded_states, "elapsed_time": elapsed_time}

    

def heuristic(pos: Tuple[int, int], end: Tuple[int, int]) -> float:
    x_distance = pos[0] - end[0]
    y_distance = pos[1] - end[1]
    return math.sqrt(x_distance ** 2 + y_distance ** 2)


def a_star_1(maze: List[List[str]], start: Tuple[int, int], end: Tuple[int, int], rows: int, cols: int):
    path_exist = False
    OPEN = []
    h_start = heuristic(start, end)
    heapq.heappush(OPEN, (h_start, 0, start))
    CLOSED = {start: 0}
    start_time = time.perf_counter()

    while OPEN:
        f, g, current = heapq.heappop(OPEN)
        if current == end:
            path_exist = True
            break

        for neighbor in get_neighbors(current, maze, rows, cols):
            if neighbor not in CLOSED:
                h_neighbor = heuristic(neighbor, end)
                CLOSED[neighbor] = g + 1
                heapq.heappush(OPEN, (g + 1 + h_neighbor, g + 1, neighbor))
            # we don't need to update g for nodes in CLOSED since every step is 1
            # we won't find a shorter path to a node in CLOSED after we add it to CLOSED
    end_time = time.perf_counter()
    elapsed_time = round((end_time - start_time) * 1000, 4)
    if path_exist:
        length = CLOSED[end]
    else:
        length = -1
    expanded_states = len(CLOSED)
    return {"algorithm": "A*", "path_exist": path_exist, "length": length, "expanded_states": expanded_states, "elapsed_time": elapsed_time}

def read_maze_linebyline():
    n, m = map(int, sys.stdin.readline().split())
    start = end = None
    maze = []
    for i in range(n):
        line = sys.stdin.readline().strip()
        maze.append(list(line))

        for j, cell in enumerate(line):
            if cell == 'S':
                start = (i, j)
            elif cell == 'T':
                end = (i, j)

    return maze, start, end, n, m

def read_maze_from_file(filename):
    maze = []
    start = end = None
    
    with open(filename, 'r') as f:
        n, m = map(int, f.readline().split())
        for i, line in enumerate(f):
            line = line.strip() 
            row = list(line)
            maze.append(row)
            
            # 查找起点和终点
            for j, cell in enumerate(row):
                if cell == 'S':
                    start = (i, j)
                elif cell == 'T':
                    end = (i, j)
    
    return maze, start, end, n, m

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--line', action='store_true', help='Read maze line by line from stdin')
    parser.add_argument('-f', '--file', type=str, help='Read maze from a file')
    parser.add_argument('-a', '--algorithm', type=str, choices=['BFS', 'astar0', 'astar'], default='astar', help='Choose the algorithm to run')
    args = parser.parse_args()

    if args.line:
        maze, start, end, rows, cols = read_maze_linebyline()
    elif args.file:
        maze, start, end, rows, cols = read_maze_from_file(args.file) 
    else:
        print("Please specify an input method: --line or --file <filename>")
        sys.exit(1)
    
    if args.algorithm == 'BFS':
        result = BFS(maze, start, end, rows, cols)
    elif args.algorithm == 'astar0':
        result = a_star_0(maze, start, end, rows, cols)
    elif args.algorithm == 'astar':
        result = a_star_1(maze, start, end, rows, cols)

    if result['path_exist']:
        output = f"""
        [{result['algorithm']}] 
            Path Exist: Yes
            Length: {result['length']}
            Expanded States: {result['expanded_states']}
            Time: {result['elapsed_time']} ms"""
    else:
        output = f"""
        [{result['algorithm']}] 
            Path Exist: No
            Length: -1
            Expanded States: {result['expanded_states']}
            Time: {result['elapsed_time']} ms"""

    print(output)