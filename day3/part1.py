import re

class Grid:
    def __init__(self, filename):
        self.grid = []
        self.part_numbers = []
        with open(filename) as f:
            for line in f:
                self.grid.append(list(line.strip()))
        for i, row in enumerate(self.grid):
            for number in re.finditer("\d+", "".join(row)):
                if self.is_part_number(i, number.start(0), number.start(0) + len(number.group(0)) - 1):
                    self.part_numbers.append(PartNumber(number.group(0)))
    
    def is_on_grid(self, row, col):
        max_row, max_col = len(self.grid) - 1, len(self.grid[0]) - 1
        return 0 <= row <= max_row and 0 <= col <= max_col
    
    def is_part_number(self, row, start_pos, end_pos):
        adjacencies = []
        # Left
        adjacencies.append((row, start_pos - 1))
        # Right
        adjacencies.append((row, end_pos + 1))
        # Corners
        adjacencies.append((row + 1, start_pos - 1))
        adjacencies.append((row - 1, start_pos - 1))
        adjacencies.append((row + 1, end_pos + 1))
        adjacencies.append((row - 1, end_pos + 1))
        # Top and Bottom
        for i in range(start_pos, end_pos + 1):
            adjacencies.append((row - 1, i))
            adjacencies.append((row + 1, i))
        
        for x, y in adjacencies:
            if self.is_on_grid(x, y):
                if self.grid[x][y] != ".":
                    return True
                
        return False

class PartNumber:
    def __init__(self, number):
        self.value = int(number)

grid = Grid("input.txt")

result = 0
for pn in grid.part_numbers:
    result += pn.value
print(result)
