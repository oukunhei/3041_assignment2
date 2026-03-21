# use Euclidean distance as heuristic function
import sys
import heapq
import queue
from typing import List, Dict, Tuple
from pathlib import Path
import time
import argparse

# bfs算法步骤：1初始化队列（加入起点）2从头部取出元素 3判断是否end，end则在parent里面统计长度 4不是end将可行邻居添加到队列
# 如果parent长度等于矩阵大小则说明没有路径
def get_neighbors(pos: Tuple[int, int], maze: List[List[str]]) -> List[Tuple[int, int]]:
    neighbors = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # 右、左、下、上
    for dx, dy in directions:
        new_x, new_y = pos[0] + dx, pos[1] + dy
        if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] != '#':
            neighbors.append((new_x, new_y))
    return neighbors

def BFS(maze: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]):
    path_exist=False
    q = queue.Queue()
    q.put(start)
    parent = {start: None}
    visited = set()
    visited.add(start)
    start_time = time.time()

    while not q.empty():
        current = q.get()
        if current == end:
            path_exist = True
            break

        for neighbor in get_neighbors(current, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                q.put(neighbor)

    end_time = time.time()
    elapsed_time = end_time - start_time
    if path_exist:
        length = 0
        while current is not None:
            current = parent[current]
            length += 1
        length -= 1  # minus the start node
    else:
        length = -1 # no path

    expanded_states = len(visited)
    
    return path_exist, length, expanded_states, elapsed_time



# A* algorithm: 1初始化堆（加入起点）
def a_star_0(start: list) -> int:
    
    return path_exist, length, expanded_states, time
    
            
def a_star_1(start: list) -> int:
    
    return path_exist, length, expanded_states, time

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

    return maze, start, end

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
    
    return maze, start, end

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--linebyline', action='store_true', help='Read maze line by line from stdin')
    parser.add_argument('--file', type=str, help='Read maze from a file')
    args = parser.parse_args()

    if args.linebyline:
        maze, start, end = read_maze_linebyline()
    elif args.file:
        maze, start, end = read_maze_from_file(args.file)
    
    else:
        print("Please specify an input method: --linebyline or --file <filename>")
        sys.exit(1)
    
    BFS_result = BFS(maze, start, end)
    print("BFS:", BFS_result)
