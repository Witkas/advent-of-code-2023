class Card:
    id = 0
    winning_numbers = []
    your_numbers = []

    def __init__(self, line):
        self.id = int(line[line.index("d") + 1:line.index(":")].strip())
        self.winning_numbers = list(map(int, line[line.index(":") + 2:line.index("|") - 1].split()))
        self.your_numbers = list(map(int, line[line.index("|") + 2:].split()))

    def get_won_ids(self):
        won_ids = []
        counter = 0
        for n in self.your_numbers:
            if n in self.winning_numbers:
                counter += 1
                won_ids.append(self.id + counter)
        return won_ids


cards = []
with open("input.txt") as f:
    for line in f:
        cards.append(Card(line.strip()))

for c in cards:
    won_ids = c.get_won_ids()
    for id in won_ids:
        cards.append(cards[id - 1])
print(len(cards))
