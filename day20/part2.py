from collections import defaultdict

lines = []
with open('input.txt') as f:
    for line in f.readlines():
        lines.append(line.strip())

# e.g. '&a': 'b, c'
connections = {}
for line in lines:
    [k, v] = line.split(" -> ")
    connections[k] = v

# Flip-Flop: On/Off (True/False)
# Conjunction: {
#   Input1: "LOW",  (False)
#   Input2: "HIGH", (True)
#   ...
# }
# e.g. 'a': False
# e.g. 'b': {'a': False}
state = {}
for input, _ in connections.items():
    # Flip-Flop
    if input[0] == '%':
        state[input[1:]] = False
    # Conjunction
    elif input[0] == '&':
        state[input[1:]] = {}
        for i, outs in connections.items():
            if input[1:] in outs:
                state[input[1:]][i[1:]] = False

# e.g. 'a': '%'
types = defaultdict(lambda: '')
for k in connections.keys():
    if k[0] == '%' or k[0] == '&':
        types[k[1:]] = k[0]
    else:
        types[k] = ''

# input: 'a'
# output: ['b', 'c']
def get_outputs(k):
    if k == 'broadcaster':
        return connections["broadcaster"].split(", ")
    return connections[types[k] + k].split(", ")

# [where from, to who, low/high]
# e.g. ['%a', '&b', True]
pulses = []
press_count = 0
while True:
    press_count += 1 # Pressing the button
    pulses.append(('button', 'broadcaster', False))
    while pulses:
        # print(pulses)
        current = pulses.pop(0)
        if current[1] == '&rg' and current[2] == True:
            print(f"{current[0]}: {press_count}")
        # Broadcaster case
        if current[1] == 'broadcaster':
            for o in get_outputs('broadcaster'):
                pulses.append(('broadcaster', types[o] + o, False))
        # Flip-Flop case
        elif current[1][0] == '%':
            # High Signal
            if current[2]:
                continue
            # Low Signal
            else:
                state[current[1][1:]] = not state[current[1][1:]]
                for o in get_outputs(current[1][1:]):
                    if state[current[1][1:]]:
                        pulses.append((current[1], types[o] + o, True))
                    else:
                        pulses.append((current[1], types[o] + o, False))
        # Conjunction case
        elif current[1][0] == '&':
            # Update memory
            state[current[1][1:]][current[0][1:]] = current[2]
            last_inputs = state[current[1][1:]].values()
            # print(f'last_inputs = {last_inputs}')
            for o in get_outputs(current[1][1:]):
                # All High
                if all(last_inputs):
                    pulses.append((current[1], types[o] + o, False))
                else:
                    pulses.append((current[1], types[o] + o, True))
        # print(state)
    
print(press_count)
