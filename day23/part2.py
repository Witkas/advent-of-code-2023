import sys
sys.setrecursionlimit(1000000)

def print_maze(maze):
    rows = [str(i).ljust(3, " ") + ''.join(x) for i, x in enumerate(maze)]
    print('\n'.join(rows))

def is_dest_reachable(new_row, new_col, visited, maze):
    last_row = len(maze) - 1
    last_col = len(maze[0]) - 1
    visited_maze = []
    for row in maze:
        visited_maze.append(row.copy())
    for visited_row, visited_col in visited:
        visited_maze[visited_row][visited_col] = '#'
    # Let's do BFS and see if we can find the destination
    bfs = [(new_row, new_col)]
    while bfs:
        x, y = bfs.pop(0)
        if x == last_row and y == last_col - 1:
            return True
        directions = [
            [-1, 0, "up"],
            [0, 1, "right"],
            [1, 0, "down"],
            [0, -1, "left"],
        ]
        for x_d, y_d, _ in directions:
            new_x, new_y = x + x_d, y + y_d
            if is_legal_move(x, y, new_x, new_y, visited, visited_maze):
                bfs.append((new_x, new_y))
                visited_maze[x][y] = '#'
    return False

def is_legal_move(row, col, new_row, new_col, visited, maze):
    last_row = len(maze) - 1
    last_col = len(maze[0]) - 1

    # Boundary check
    if new_row < 0 or new_row > last_row or new_col < 0 or new_col > last_col:
        return False
    
    # Forests
    if maze[new_row][new_col] == '#':
        return False
    
    # Slopes
    if maze[row][col] == '^':
        if not row - 1 == new_row:
            return False
    if maze[row][col] == '>':
        if not col + 1 == new_col:
            return False
    if maze[row][col] == 'v':
        if not row + 1 == new_row:
            return False
    if maze[row][col] == '<':
        if not col - 1 == new_col:
            return False
        
    # Previously visited squares
    if (new_row, new_col) in visited:
        return False
    
    # Check if we can reach the destination without 
    # stepping on any of the previous squares.
    return True

def longest_path(row, col, memo, visited, maze):
    directions = [
        [-1, 0, "up"],
        [0, 1, "right"],
        [1, 0, "down"],
        [0, -1, "left"],
    ]
    lengths = []
    for row_d, col_d, dir_name in directions:
        new_row, new_col = row + row_d, col + col_d
        if is_legal_move(row, col, new_row, new_col, visited, maze) and is_dest_reachable(new_row, new_col, visited, maze):
            maze[row][col] = "O" # Debugging
            if (new_row, new_col, dir_name) not in memo:
                visited[(new_row, new_col)] = True
                memo[(new_row, new_col, dir_name)] = longest_path(new_row, new_col, memo, visited, maze)
                del visited[(new_row, new_col)]
            # Debugging
            # else:
            #     print_maze(maze)
            #     print(f"Entry in memo for {new_row},{new_col}: {memo[(new_row, new_col, dir_name)]}")
            #     print()
            if memo[(new_row, new_col, dir_name)] == 5:
                print_maze(maze)
                print()
            lengths.append(memo[(new_row, new_col, dir_name)]) 
            maze[row][col] = "."
    return max(lengths) + 1

maze = []
with open("test.txt") as f:
    for line in f:
        maze.append(list(line.strip()))

# for row in maze:
#     for i, char in enumerate(row):
#         if char in "^>v<":
#             row[i] = "."

last_row = len(maze) - 1
last_col = len(maze[0]) - 1
print(longest_path(0, 1, {(last_row, last_col - 1, "down"): 0}, {(0, 1): True}, maze))
