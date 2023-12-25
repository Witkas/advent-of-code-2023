import re

def lines():
    with open("input.txt") as f:
        yield from f

def convert(x):
    if len(x) == 1:
        return x
    return {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }[x]

result = []
for line in lines():
    first = re.search("one|two|three|four|five|six|seven|eight|nine|[0-9]", line)
    last = re.search("[0-9a-z]*(one|two|three|four|five|six|seven|eight|nine|[0-9])", line)
    result.append(int(convert(first.group(0)) + convert(last.group(1))))
print(sum(result))
