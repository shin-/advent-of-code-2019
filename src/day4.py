code_range = (356261, 846304)

part1_count = 0
part2_count = 0
for num in range(*code_range):
  digits = [int(x) for x in str(num)]
  has_adjacents = False
  groups = {}
  for index, d in enumerate(digits):
    if index < 5:
      if digits[index + 1] == d:
        has_adjacents = True
        groups[d] = groups[d] + 1 if d in groups else 2
      if digits[index + 1] < d:
        break
  if index == 5 and has_adjacents:
    part1_count += 1
    if any([c == 2 for c in groups.values()]):
      part2_count += 1

print(f'Part 1 count: {part1_count}, Part 2 count: {part2_count}')
