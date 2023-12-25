import re

class Grid:
    def __init__(self, filename):
        self.grid = []
        self.part_numbers = []
        self.gears = []
        with open(filename) as f:
            for line in f:
                self.grid.append(list(line.strip()))
        for i, row in enumerate(self.grid):
            for number in re.finditer("\d+", "".join(row)):
                if self.is_part_number(i, number.start(0), number.start(0) + len(number.group(0)) - 1):
                    self.part_numbers.append(PartNumber(number.group(0), i, number.start(0)))
        for i, row in enumerate(self.grid):
            for star in re.finditer("\*", "".join(row)):
                if self.is_gear(i, star.start(0)):
                    pn1, pn2 = self.get_part_numbers_for_gear(i, star.start(0))
                    self.gears.append(Gear(pn1, pn2))
    
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
    
    def get_part_number(self, row, col):
        for pn in self.part_numbers:
            if pn.row == row and pn.start_pos <= col <= pn.end_pos:
                return pn
    
    def is_gear(self, row, col):
        part_numbers = self.get_part_numbers_for_gear(row, col)
        if len(part_numbers) != 2:
            return False
        return True

    def get_part_numbers_for_gear(self, row, col):
        adjacencies = [
            [-1, -1],
            [-1, 0],
            [-1, 1],
            [0, -1],
            [0, 1],
            [1, -1],
            [1, 0],
            [1, 1],
        ]
        part_numbers = []
        for x, y in adjacencies:
            if self.is_on_grid(row + x, col + y):
                if self.grid[row + x][col + y] in "0123456789":
                    pn = self.get_part_number(row + x, col + y)
                    if not pn in part_numbers:
                        part_numbers.append(pn)
        return part_numbers

class PartNumber:
    def __init__(self, number, row, col):
        self.value = int(number)
        self.row = row
        self.start_pos = col
        self.end_pos = col + len(number) - 1

class Gear:
    def __init__(self, pn1, pn2):
        self.ratio = pn1.value * pn2.value

grid = Grid("input.txt")

result = 0
for g in grid.gears:
    result += g.ratio
print(result)
