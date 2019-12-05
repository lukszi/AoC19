import math

with open("parts.txt") as f:
    parts = list(map(int, f.readlines()))
parts_with_fuel = parts.copy()
weight = 0
i = 0
while i < len(parts_with_fuel):
    weight = math.floor(parts_with_fuel[i]/3) - 2
    parts_with_fuel.insert(i+1, weight)
    i = i+2
print("part 1: ", sum(parts_with_fuel))

parts_with_fuel = parts.copy()
weight = 0
i = 0
while i < len(parts_with_fuel):
    weight = math.floor(parts_with_fuel[i]/3) - 2
    if weight > 0:
        parts_with_fuel.insert(i+1, weight)
    i = i+1
print("part 2: ", sum(parts_with_fuel) - sum(parts))
