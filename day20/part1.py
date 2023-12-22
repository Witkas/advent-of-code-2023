class Stats:
    low_count = 0
    high_count = 0

    def result(self):
        return self.low_count * self.high_count
    
stats = Stats()

class Clock:
    ready = []

    def cycle(self):
        actions, self.ready = self.ready, []
        for src, dest, level in actions:
            if level == "low":
                stats.low_count += 1
            else:
                stats.high_count += 1
            # print(f"{src.name}-{level}>{dest.name}")
            dest.send_pulse(src, level)

clock = Clock()
    
class Component:
    name = ''
    dests = []
    state = None

    def __init__(self, name, dests):
        self.name = name[1:] if name[0] in "%&" else name
        self.dests = dests
    
    def send_pulse(self, src, level):
        pass

class Button(Component):
    broadcaster = None
    def __init__(self, broadcaster):
        self.broadcaster = broadcaster

    def press(self):
        clock.ready.append([self, self.broadcaster, "low"])

class Broadcaster(Component):
    def send_pulse(self, src, level):
        for d in self.dests:
            clock.ready.append([self, d, "low"])

class Flipflop(Component):
    def __init__(self, name, dests):
        super().__init__(name, dests)
        self.state = "off"

    def send_pulse(self, src, level):
        if level == "high":
            return
        self.state = {"on": "off", "off": "on"}[self.state]
        out_level = {"on": "high", "off": "low"}[self.state]
        for d in self.dests:
            clock.ready.append([self, d, out_level])

class Conjunction(Component):
    def __init__(self, name, dests):
        super().__init__(name, dests)
        self.state = {}
    
    def add_input(self, input):
        self.state[input] = "low"

    def send_pulse(self, src, level):
        self.state[src] = level
        out_level = "low" if all(x == "high" for x in self.state.values()) else "high"
        for d in self.dests:
            clock.ready.append([self, d, out_level])

components = {}
file = 'input.txt'
with open(file) as f:
    for line in f:
        src, dests = line.strip().split(" -> ")
        dests = dests.split(", ")
        if src == "broadcaster":
            components["broadcaster"] = Broadcaster("broadcaster", dests)
        if src[0] == "%":
            components[src[1:]] = Flipflop(src[1:], dests)
        if src[0] == "&":
            components[src[1:]] = Conjunction(src[1:], dests)
# Look for the outputs that don't pass the 
# signal further (e.g. 'output' in test2.txt).
with open(file) as f:
    for line in f:
        _, dests = line.strip().split(" -> ")
        dests = dests.split(", ")
        for d in dests:
            if d not in components:
                components[d] = Component(d, [])

for c in components.values():
    c.dests = [components[d] for d in c.dests]

for c in components.values():
    for d in c.dests:
        if isinstance(d, Conjunction):
            d.add_input(c)

button = Button(components["broadcaster"])
for _ in range(1000):
    button.press()
    while clock.ready:
        clock.cycle()

print(stats.result())
        