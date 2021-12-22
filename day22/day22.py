import numpy as np
import re

to_slice = lambda c : np.s_[c[0]:c[1]+1, c[2]:c[3]+1]

rX, rY, rZ = np.s_[0:2], np.s_[2:4], np.s_[4:6]

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

def get_size(cube):
	return (cube[1]-cube[0]+1) * (cube[3]-cube[2]+1)# * (cube[5]-cube[4]+1)

def does_intersect(a, b):
	a, b = sorted(a), sorted(b)
	return a[0] <= b[0] <= a[1] or b[0] <= a[0] <= b[1]
def cubes_intersect(c1, c2):
	return does_intersect(c1[rX], c2[rX]) and does_intersect(c1[rY], c2[rY])

def does_overlap(a, b):
	a, b = sorted(a), sorted(b)
	return (a[0] <= b[0] and b[1] <= a[1])# or (b[0] <= a[0] and a[1] <= b[1])
def cubes_overlap(c1, c2):
	return (does_overlap(c1[rX], c2[rX]) and does_overlap(c1[rY], c2[rY]))

def get_ranges(cubes, clip=None):
	if type(cubes) != np.array: cubes = np.array(cubes)
	mins = np.min(cubes[:,  ::2], axis=0)
	maxs = np.max(cubes[:, 1::2], axis=0)
	if clip:
		mins = np.clip(mins, -clip, clip)
		maxs = np.clip(maxs, -clip, clip)
	
	return list(np.stack([mins, maxs]).T.flatten())

def print_matrix(matrix):
	for row in matrix.T:
		print("".join([ [".", "#"][c] for c in row ]))

def print_cubes(cubes):
	if type(cubes) != np.array: cubes = np.array(cubes)

	ranges = xmin, xmax, ymin, ymax = get_ranges(cubes)
	width, height= xmax-xmin+1, ymax-ymin+1

	padding=0
	width, height = xmax+3, ymax+3
	string = ["."*(width+padding*2)] * (height+padding*2)

	for i_cube, cube in enumerate(cubes):
		x1, x2, y1, y2 = cube
		for x in range(x1, x2+1):
			for y in range(y1, y2+1):
				string[y+padding] = string[y+padding][:x+padding] + "123456789ABCDEFGHIJKLMNOP"[i_cube] + string[y+padding][x+padding+1:]
	
	total = sum([ get_size(cube) for cube in cubes ])
	print()
	print("\n".join(string))
	print("Total:", total)

def subtract(c1, c2):
	print("[subtract]", c1, c2)

	print_cubes([c1,c2])
	if not cubes_intersect(c1, c2): return [c1]

	# x1a => x2a, x2a => x2b, x2b=>x1b
	xs = [ [c1[0], c2[0]-1], [c2[0], c2[1]], [c2[1]+1, c1[1]] ]
	ys = [ [c1[2], c2[2]-1], [c2[2], c2[3]], [c2[3]+1, c1[3]] ]

	cubes = []
	counter = 0
	for x1, x2 in xs:
		for y1, y2 in ys:
			# Even though x1, y1, etc, are integers, these are still passed by reference for whatever reason
			# print(f"{counter} : x{x1,x2}, y{y1,y2}", c2[0], c2[1])
			if x1 == c2[0] and y1 == c2[2]: continue

			if x2 < x1 : continue
			if y2 < y1 : continue
			counter += 1
			
			x1_ = np.clip(x1, c1[0], c1[1])
			x2_ = np.clip(x2, c1[0], c1[1])
			y1_ = np.clip(y1, c1[2], c1[3])
			y2_ = np.clip(y2, c1[2], c1[3])

			# print(counter, x1, "=>", x2, y1, "=>", y2)

			cubes.append([x1_,x2_,y1_,y2_])
			
	# cubes.pop(len(cubes)//2)
	print_cubes(cubes)
	return [ list(c) for c in cubes ]

def add(c1, c2):
	# Check for complete overlap
	print("c1 in c2 :", cubes_intersect(c1, c2))

	if cubes_overlap(c1, c2): return np.array([c1])
	if cubes_overlap(c2, c1): return np.array([c2])

	xs = [ [c1[0], c2[0]-1], [c2[0], c1[1]], [c1[1]+1, c2[1]] ]
	ys = [ [c1[2], c2[2]-1], [c2[2], c1[3]], [c1[3]+1, c2[3]] ]

	cubes = []
	counter = 0
	print(xs)
	print(ys)
	for x1, x2 in xs:
		for y1, y2 in ys:
			cubes.append([x1, x2, y1, y2])
	return np.array(cubes)


def add_(c1, c2):
	if not cubes_intersect(c1,c2):
		return np.array([c1, c2])

	if cubes_overlap(c1, c2): return np.array([c1])
	if cubes_overlap(c2, c1): return np.array([c2])

	xs = sorted(list(c1[0:2]) +  list(c2[0:2]))
	ys = sorted(list(c1[2:4]) +  list(c2[2:4]))
	print(xs, ys)

	xs = [ [xs[0], xs[1]-1], [xs[1], xs[2]], [xs[2]+1, xs[3]] ]
	ys = [ [ys[0], ys[1]-1], [ys[1], ys[2]], [ys[2]+1, ys[3]] ]
	print(xs)

	cubes = []
	counter = 0
	for x1, x2 in xs:
		for y1, y2 in ys:
			cubes.append([x1, x2, y1, y2])

	cubes = [ c for c in cubes if not cubes_intersect(c1, c) and cubes_intersect(c2, c) ]
	return c1, np.array(cubes)

	cubes = [ c for c in cubes if cubes_intersect(c1, c) or cubes_intersect(c2, c) ]
	return np.array(cubes)


enabled, cubes = get_input("input_small.txt")
cubes = cubes[:, :4]

# cubes = np.array([ [0,5,0,5], [4,8,4,8], [2,6,2,6] ])
# enabled = [True, False, True]
cubes_original = np.copy(cubes)

ranges = xmin, xmax, ymin, ymax = get_ranges(cubes)
width, height = xmax-xmin+1, ymax-ymin+1
print(width, height)

cubes[:, 0:2] -= xmin
cubes[:, 2:4] -= ymin

cubes = [ list(cube) for cube in cubes ]

print(cubes)
print(enabled)

matrix = np.zeros((width, height), dtype=bool)

print_cubes(cubes)

# turned_on, turned_off = [], []
# for is_on, cube in list(zip(enabled, cubes)):
# 	matrix[to_slice(cube)] = is_on
# 	if is_on : turned_on.append(cube)
# 	else     : turned_off.append(cube)

existing_cubes = []
cubes = list(cubes)
print("\n=========")

for i_cube, [is_on, cube] in enumerate(zip(enabled, cubes)):
	print(f"\n\n===========================\n{i_cube} @ {cube} = {is_on}")
	if len(existing_cubes):print_cubes(existing_cubes)
	if not is_on:
		existing_cubes_next = []
		print(f"Subtracting cube from {len(existing_cubes)}")
		for ecube in existing_cubes:
			existing_cubes_next += subtract(ecube, cube)
		print("After subtraction:", existing_cubes_next)
		existing_cubes = existing_cubes_next[:]

	if is_on:
		remaining_cubes = [cube[:]]
		print(f"Adding cube {remaining_cubes}")

		# For each cube that already exist in the new universe
		for ecube in existing_cubes:
			print("At existing cube", ecube)
			remaining_cubes_next = []
			# For each cube that we're trying to add
			for rcube in remaining_cubes:
				cubes_after_sub = subtract(rcube, ecube)
				remaining_cubes_next += list(cubes_after_sub)
			remaining_cubes = remaining_cubes_next[:]
			print_cubes(remaining_cubes)

		print("remaining_cubes", [list(x) for x in remaining_cubes])		
		existing_cubes += remaining_cubes

	print()
print_cubes(existing_cubes)
print_cubes([cubes_original[0], cubes_original[2]])
exit()


to_slice = lambda c : np.s_[c[0]:c[1]+1, c[2]:c[3]+1, c[4]:c[5]+1]



def get_ranges(cubes, clip=None):
	if type(cubes) != np.array: cubes = np.array(cubes)
	mins = np.min(cubes[:,  ::2], axis=0)
	maxs = np.max(cubes[:, 1::2], axis=0)
	if clip:
		mins = np.clip(mins, -clip, clip)
		maxs = np.clip(maxs, -clip, clip)
	
	return list(np.stack([mins, maxs]).T.flatten())

enabled, cubes = get_input("input_small.txt")
print(cubes)
ranges = xmin, xmax, ymin, ymax, zmin, zmax = get_ranges(cubes)
width, height, depth = xmax-xmin+1, ymax-ymin+1, zmax-zmin+1

print(width, height, depth, width*height*depth/ 10**9)
exit()
cubes[:, 0:2] -= xmin
cubes[:, 2:4] -= ymin
cubes[:, 4:6] -= zmin
exit()
matrix = np.zeros((width, height, depth), dtype=bool)

for is_on, cube in list(zip(enabled, cubes)):
	c = cube
	print(is_on, cube, to_slice(cube))
	matrix[to_slice(cube)] = is_on

print(matrix)

print(np.sum(matrix))