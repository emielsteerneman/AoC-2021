import numpy as np
coordinates, instructions = open("input.txt").read().strip().split("\n\n")

instructions = [ instruction.split(" ")[-1].split("=") for instruction in instructions.split("\n") ]
coordinates = np.array([ list(map(int, line.split(","))) for line in coordinates.strip().splitlines()])

max_x = np.max(coordinates[:, 0])
max_y = np.max(coordinates[:, 1])

paper = np.zeros((max_y+1, max_x+1), dtype=bool)
for x, y in coordinates: paper[y, x] = True

for i_instruction, (axis, n) in enumerate(instructions):
	n = int(n)

	if axis == 'y':
		a, b = paper[:n, :], paper[-n:, :]
		paper = a | np.flipud(b)

	if axis == 'x':
		a, b = paper[:, :n], paper[:, -n:]		
		paper = a | np.fliplr(b)

	if i_instruction == 0:
		print("Part 1 :", np.sum(paper))

paper_string = "\n".join([ "".join([ "██" if v else "  " for v in row ]) for row in paper ])
print(paper_string)