import numpy as np

file = open("input.txt").read().strip().split("\n")

height, width = len(file), len(file[0])
matrix = np.zeros((height, width))
for (y, x), i in np.ndenumerate(matrix):
	matrix[y, x] = ".>v".index(file[y][x])


def step(matrix, X):
	height, width = matrix.shape
	for y in range(height):
		row = matrix[y]
		skip = -1
		row_ = np.copy(row)
		for x in range(width):
			if x == skip: continue
			if row[x] != X: continue
			xd = (x+1)%width
			if row_[xd] != 0: continue

			row[x] = 0
			row[xd] = X
			skip = xd

epoch = 0
while True:
	epoch += 1
	prev_matrix = np.copy(matrix)

	step(matrix, 1)
	step(matrix.T, 2)
	
	if np.array_equal(prev_matrix, matrix):
		print("Part 1:", epoch)
		break