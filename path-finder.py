import curses
from curses import wrapper
import queue
import time

maze = [
    ["#", "", "#", "#", "#", "#", "O", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]


def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j
    return None


def find_neighbors(maze, row, col):
    neighbors = []

    if row > 0:  # UP
        neighbors.append((row - 1, col))
    if row + 1 < len(maze):  # DOWN
        neighbors.append((row + 1, col))
    if col > 0:  # LEFT
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):  # RIGHT
        neighbors.append((row, col + 1))

    return neighbors


def find_path(maze, stdscr=None):
    start = "O"
    end = "X"
    obstacle = "#"

    start_pos = find_start(maze, start)
    bfs_q = queue.Queue()
    visited = set()

    bfs_q.put((start_pos, [start_pos]))

    while not bfs_q.empty():
        current_pos, path = bfs_q.get()
        row, col = current_pos

        stdscr.clear()
        print_maze(maze, stdscr, path)
        time.sleep(0.2)
        stdscr.refresh()

        if maze[row][col] == end:
            return path

        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            r, c = neighbor
            if maze[r][c] == obstacle:
                continue
            new_path = path + [neighbor]
            bfs_q.put((neighbor, new_path))
            visited.add(neighbor)


def print_maze(maze, stdscr, path=[]):
    GREEN = curses.color_pair(1)
    BLUE = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j, "-", GREEN)
            else:
                stdscr.addstr(i, j, value, BLUE)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)

    find_path(maze, stdscr)
    stdscr.getch()


wrapper(main)
