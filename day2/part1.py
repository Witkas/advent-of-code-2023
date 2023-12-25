games = []
with open("input.txt") as f:
    for line in f:
        maximums = {
            "red": 0,
            "green": 0,
            "blue": 0, 
        }
        line = line[line.index(":")+2:].strip().split("; ")
        for draw in line:
            draw = draw.split(", ")
            for ball in draw:
                quantity, color = ball.split()
                maximums[color] = max(maximums[color], int(quantity))
        games.append(maximums)

result = 0
for i, game in enumerate(games):
    if game["red"] <= 12 and game["green"] <= 13 and game["blue"] <= 14:
        result += i + 1
print(result)
