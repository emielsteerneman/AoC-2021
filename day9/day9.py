import numpy as np

text = open("input.txt").read().strip().split("\n")
H, W = len(text), len(text[0])

# Fill matrix
matrix = np.array([[ int(x) for x in row ] for row in text ])
# Fill outer matrix, to make kernel work
outer_matrix = np.pad(matrix, pad_width=1, constant_values=9)



# Part 1 & 2
local_minima = []



# Part 1
kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])

for (i, j), x in np.ndenumerate(matrix):
	# Get 3x3 ROI matrix
	ROI = outer_matrix[i:i+3,j:j+3]
	# Apply kernel, apply x< condition
	if np.all(x < ROI[kernel > 0]): 
		local_minima.append((i, j))

total = sum([ matrix[p] + 1 for p in local_minima ])
print("Part 1 :", total)
print("Part 1 :", sum([ matrix[(i, j)] + 1 for (i, j), x in np.ndenumerate(matrix) if np.all(x < outer_matrix[i:i+3,j:j+3][np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]) > 0]) ]))



# Part 2
basin_sizes = []
for i, j in local_minima:

	basin_size, visited, queued = 0, [], [(i, j)]

	# While positions are in the queue
	while 0 < len(queued):
		# Grab position
		i, j = queued.pop(0)
		# Skip if visited
		if (i, j) in visited: continue
		# Skip if out of area
		if i < 0 or j < 0 or H <= i or W <= j: continue
		# Add to visited
		visited.append((i, j))
		# Skip if wall
		if matrix[i, j] == 9: continue

		# Increase basin size
		basin_size += 1
		# Add neighbours to queue
		queued.append((i-1, j))
		queued.append((i+1, j))
		queued.append((i, j-1))
		queued.append((i, j+1))

	basin_sizes.append(basin_size)

total = np.prod(sorted(basin_sizes)[-3:])
print("Part 2 :", total)