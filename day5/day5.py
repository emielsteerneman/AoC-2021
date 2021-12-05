import re
import numpy as np
import cv2

lines = open("input.txt").read().split("\n")
inputs = [ list(map(int, re.findall(r"\d+", line))) for line in lines ]

size = 10 if len(inputs) < 100 else 1000

grid = np.zeros((size, size), dtype=np.uint8)
for x1, y1, x2, y2 in inputs:
	if x1 != x2 and y1 != y2: continue
	grid_ = np.zeros((size, size), dtype=np.uint8)
	cv2.line(grid_, (x1, y1), (x2, y2), 1, 1)
	grid += grid_
print(np.sum(1 < grid))

grid = np.zeros((size, size), dtype=np.uint8)
for x1, y1, x2, y2 in inputs:
	grid_ = np.zeros((size, size), dtype=np.uint8)
	cv2.line(grid_, (x1, y1), (x2, y2), 1, 1)
	grid += grid_
print(np.sum(1 < grid))

# # Part 1
# grid = np.zeros((size, size), dtype=np.uint64)
# for x1, y1, x2, y2 in inputs:
# 	if y1 == y2:
# 		xmin, xmax = sorted([x1, x2])
# 		for x in range(xmin, xmax+1):
# 			grid[y1, x] += 1

# 	if x1 == x2:
# 		ymin, ymax = sorted([y1, y2])
# 		for y in range(ymin, ymax+1):
# 			grid[y, x1] += 1
# print(np.sum(1 < grid))

# # Part 2
# grid = np.zeros((size, size), dtype=np.uint64)
# for x1, y1, x2, y2 in inputs:

# 	xmin, xmax = sorted([x1, x2])
# 	ymin, ymax = sorted([y1, y2])
	
# 	if ymin == ymax:
# 		for x in range(xmin, xmax+1):
# 			grid[y1, x] += 1

# 	elif xmin == xmax:
# 		for y in range(ymin, ymax+1):
# 			grid[y, x1] += 1

# 	elif xmin != xmax and ymin != ymax:
# 		xd = 1 if x1 < x2 else -1
# 		yd = 1 if y1 < y2 else -1

# 		while x1 != x2:			
# 			grid[y1, x1] += 1
# 			x1 += xd
# 			y1 += yd
# print(np.sum(1 < grid))