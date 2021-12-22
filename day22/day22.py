import numpy as np
import time
import re

rX, rY, rZ = np.s_[0:2], np.s_[2:4], np.s_[4:6]
rXY, rYZ = np.s_[0:4], np.s_[2:6]

def get_input(filename):
	lines = open(filename).read().strip().split("\n")
	lines = [ line.split(" ") for line in lines ]

	enabled, cubes = [], []
	for on_str, cube_str in lines:
		on = on_str == "on"
		enabled.append(on)
		cube = re.findall(r'-?\d+', cube_str)
		cube = list(map(int, cube))
		cubes.append(cube)

	return enabled, np.array(cubes)

def merge_cubes(c1, c2):
	if c1[rX] == c2[rX] and c1[rY] == c2[rY]:
		if c1[5]+1 == c2[4]: return [c1[rXY] + [c1[4], c2[5]]]
		if c2[5]+1 == c1[4]: return [c1[rXY] + [c2[4], c1[5]]]
	
	if c1[rX] == c2[rX] and c1[rZ] == c2[rZ]:
		if c1[3]+1 == c2[2]: return [c1[rX] + [c1[2], c2[3]] + c1[rZ]]
		if c2[3]+1 == c1[2]: return [c1[rX] + [c2[2], c1[3]] + c1[rZ]]
	
	if c1[rY] == c2[rY] and c1[rZ] == c2[rZ]:
		if c1[1]+1 == c2[0]: return [[c1[0], c2[1]] + c1[rYZ]]
		if c2[1]+1 == c1[0]: return [[c2[0], c1[1]] + c1[rYZ]]
	return [c1, c2]

def merge_all_cubes(cubes):
	# While cubes can still be merged
	while True:
		n_merged = 0
		is_merged = [False] * len(cubes)
		new_cubes = []

		# Try to merge each combination of cubes
		for i1 in range(len(cubes)):
			for i2 in range(len(cubes)):
				# If one of the cubes has already been merged this iteration, skip
				if is_merged[i1] or is_merged[i2]: continue
				# Try to merge the cubes
				merged = merge_cubes(cubes[i1], cubes[i2])
				# If two cubes result in one cube
				if len(merged) == 1: 
					# Set both cubes to merged
					is_merged[i1] = True
					is_merged[i2] = True
					# Store newly merged cube
					new_cubes += merged
					n_merged += 1

		# Add all cubes that have not been merged
		for i in range(len(cubes)):
			if not is_merged[i]:
				new_cubes.append(cubes[i])
		cubes = new_cubes

		# If no cubes have been merged, break
		if n_merged == 0:
			break
	return cubes

def get_volume(cube):
	return (cube[1]-cube[0]+1) * (cube[3]-cube[2]+1) * (cube[5]-cube[4]+1)

def does_intersect(a, b):
	return a[0] <= b[0] <= a[1] or b[0] <= a[0] <= b[1]
def cubes_intersect(c1, c2):
	return does_intersect(c1[rX], c2[rX]) and does_intersect(c1[rY], c2[rY]) and does_intersect(c1[rZ], c2[rZ])

def does_overlap(a, b):
	return (a[0] <= b[0] and b[1] <= a[1])
def cubes_overlap(c1, c2):
	return does_overlap(c1[rX], c2[rX]) and does_overlap(c1[rY], c2[rY]) and does_overlap(c1[rZ], c2[rZ])

def get_ranges(cubes):
	if type(cubes) != np.array: cubes = np.array(cubes)
	mins = np.min(cubes[:,  ::2], axis=0)
	maxs = np.max(cubes[:, 1::2], axis=0)
	return list(np.stack([mins, maxs]).T.flatten())

def subtract(c1, c2):
	# If c2 completely overlaps c1
	if cubes_overlap(c2, c1): return []
	# If c2 doesn't touch c1
	if not cubes_intersect(c1, c2): return [c1]

	xs = [ [c1[0], c2[0]-1], [c2[0], c2[1]], [c2[1]+1, c1[1]] ]
	ys = [ [c1[2], c2[2]-1], [c2[2], c2[3]], [c2[3]+1, c1[3]] ]
	zs = [ [c1[4], c2[4]-1], [c2[4], c2[5]], [c2[5]+1, c1[5]] ]

	cubes = []
	for x1, x2 in xs:
		for y1, y2 in ys:
			for z1, z2 in zs:
				if x1 == c2[0] and y1 == c2[2] and z1 == c2[4]: continue

				if x2 < x1 : continue
				if y2 < y1 : continue
				if z2 < z1 : continue
				
				x1_ = np.clip(x1, c1[0], c1[1])
				x2_ = np.clip(x2, c1[0], c1[1])
				y1_ = np.clip(y1, c1[2], c1[3])
				y2_ = np.clip(y2, c1[2], c1[3])
				z1_ = np.clip(z1, c1[4], c1[5])
				z2_ = np.clip(z2, c1[4], c1[5])

				cubes.append([x1_,x2_,y1_,y2_,z1_,z2_])

	# Merge a maximum of 8 cubes into fewer cubes
	return merge_all_cubes([ list(c) for c in cubes ])

def run(enabled, cubes):
	# Normalize cubes
	ranges = xmin, xmax, ymin, ymax, zmin, zmax = get_ranges(cubes)
	cubes[:, rX] -= xmin
	cubes[:, rY] -= ymin
	cubes[:, rZ] -= zmin
	cubes = [ list(cube) for cube in cubes ]

	existing_cubes = []
	t_start = time.time()*1000

	# For each cube
	for i_cube, [is_on, cube] in enumerate(zip(enabled, cubes)):

		# If the cube has to be subtracted
		if not is_on:
			existing_cubes_next = []
			# Subtract this cube from every other cube already existing
			for existing_cube in existing_cubes:
				existing_cubes_next += subtract(existing_cube, cube)
			# Set the cubes that are currently existing
			existing_cubes = existing_cubes_next

		# If the cube has to be added
		if is_on:
			# Start with the cube that has to be added
			remaining_cubes = [cube]
			# For each cube that already exist in the new universe
			for ecube in existing_cubes:
				remaining_cubes_next = []
				# For each cube that we're adding
				for rcube in remaining_cubes:
					# Subtract the already existing cubes from the cube we're adding
					cubes_after_sub = subtract(rcube, ecube)
					# Store the leftover cubes
					remaining_cubes_next += list(cubes_after_sub)
				remaining_cubes = remaining_cubes_next[:]
			# Add the cubes that remain after subtraction to all existing cubes
			existing_cubes += remaining_cubes

	total_size = sum([get_volume(c) for c in existing_cubes])
	t_stop = time.time()*1000
	duration = int(t_stop-t_start)

	return total_size, duration

enabled, cubes = get_input("input1.txt")
clip_cube = [-50, 50, -50, 50, -50, 50]
cubes = np.array([ c for c in cubes if cubes_intersect(c, clip_cube) ])
cubes = np.clip(cubes, -50, 50) #513743
cubes_original = np.copy(cubes)
total_volume, duration = run(enabled, cubes)
print(f"Part 1: {total_volume} ({duration}ms)")

enabled, cubes = get_input("input2.txt")

total_volume, duration = run(enabled, cubes)
print(f"Part 2: {total_volume} ({duration}ms)")
