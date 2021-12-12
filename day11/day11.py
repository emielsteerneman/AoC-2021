import numpy as np

text = open("input.txt").read().strip().split("\n")				# Load input
matrix = np.array([[ int(x) for x in row ] for row in text ])	# Fill matrix
outer_matrix = np.pad(matrix, pad_width=1, constant_values=9)	# Fill outer matrix, to make indexing work
matrix = outer_matrix[1:-1, 1:-1]								# Restore reference

n_flashes = 0

for i_epoch in range(1000):
	# Increment all octopuses
	matrix += 1
	# Matrix to keep track of which octopuses already flashed
	flash_matrix = np.zeros(matrix.shape, dtype=bool)

	while True:									# While flashes are still occuring
		flash_sum = np.sum(flash_matrix)			# Number of flashes before updating
		for (i, j), x in np.ndenumerate(matrix):	# For each octopus
			if x < 10 or flash_matrix[i, j]: continue	# Skip if octopus < 10 or if it already flashed
			flash_matrix[i, j] = True 					# Set octopus flashed
			outer_matrix[i:i+3,j:j+3] += 1 				# Increment surrounding octopuses
		if np.sum(flash_matrix) == flash_sum: break	# Break if no more flashes occured

	indices = 10 <= matrix 		# Get octopuses that flashed
	n_flashes += np.sum(indices)# Increment total number of flashes
	matrix[indices] = 0 		# Reset flashed octopuses to 0

	if i_epoch == 99:
		print("Part 1 :", n_flashes)

	if np.sum(matrix) == 0:
		print("Part 2 :", i_epoch + 1)
		exit()