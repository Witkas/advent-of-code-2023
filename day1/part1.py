instructions = []
with open('input.txt') as f:
    for line in f:
        instructions.append(line)

values = []
for i in instructions:
    first, last = None, None
    for c in i:
        if c in "123456789":
            if first is None:
                first = c
                last = c
            else:
                last = c
    values.append(int(first + last))
print(sum(values))
