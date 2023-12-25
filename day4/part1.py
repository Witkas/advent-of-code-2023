class Card:
    winning_numbers = []
    your_numbers = []

    def __init__(self, line):
        self.winning_numbers = list(map(int, line[line.index(":") + 2:line.index("|") - 1].split()))
        self.your_numbers = list(map(int, line[line.index("|") + 2:].split()))

    def get_points(self):
        points = 0
        for n in self.your_numbers:
            if n in self.winning_numbers:
                points = points * 2 if points > 0 else 1
        return points


cards = []
with open("input.txt") as f:
    for line in f:
        cards.append(Card(line.strip()))

result = 0
for c in cards:
    result += c.get_points()
print(result)
