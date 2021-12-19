import numpy as np
import itertools
import re

p = lambda a : " | ".join([ str(x[0]).rjust(6) + str(x[1]).rjust(6) + str(x[2]).rjust(6) for x in a])

transformations = list(itertools.product([-1, 1], repeat=3))
transformations = list(map(np.array, transformations))
T = transformations

permutations = list(itertools.permutations([0, 1, 2]))
permutations = list(map(np.array, permutations))
P = permutations

## Create all rotational matrices
R = list(itertools.product([-1, 0, 1], repeat=9))
R = [np.array(r).reshape((3, 3)) for r in R]
R = [ m for m in R if np.linalg.det(m) == 1 ]
R = [ m for m in R if ( m.T == np.linalg.inv(m) ).all() ]
print("Number of rotational matrices:", len(R))

def rotate(x):
	return np.array([ r.dot(x) for r in R ])

inv = np.linalg.inv

def get_input():
	file = open("input.txt").read().replace("\n\n", "\n").strip()
	scanners = re.split(r"---.*---\n", file)[1:]
	scanners = [ scanner.strip().split("\n") for scanner in scanners]

	scanners_ = []

	for scanner in scanners:
		scanner_ = np.array([ list(map(int, line.split(","))) for line in scanner ])
		scanners_.append(scanner_)

	return np.array(scanners_)

scanners = get_input()

# X = np.array([[-618,-824,-621], [-537,-823,-458], [-447,-329,318]])
# Y = np.array([[686,422,578],[605,423,415],[515,917,-361]])

# X = scanners[1]
# Y = scanners[4]
#WELLSHIT

def figure_it_out(X, Y):
	distances = {}

	for i_x, x in enumerate(X):
		for i_y, y in enumerate(Y):
			for i_r, r in enumerate(R):
				distance = x - r.dot(y)
				# print(i_x, i_y, i_r, r.dot(x), y, distance)
				s = str(distance)
				if s not in distances: distances[s] = [0, r, distance]
				distances[s][0] += 1

	d_list = [ [v, k] for k, v in distances.items() if 12 <= v[0]]

	if len(d_list) == 0: 
		return False, None, None

	[count, rotation, distance], string = d_list[0]
	# print("Offset:", np.linalg.inv(rotation).dot(distance))
	return True, distance, rotation


aligned_with_0 = [True] + [False] * (len(scanners) - 1)
rot_to_0 = [np.eye(3)] + [None] * (len(scanners) - 1)
offset_to_0 = [np.zeros(3, dtype=int)] + [None] * (len(scanners) - 1)


while False in aligned_with_0:
	for i1 in range(len(scanners)):
		for i2 in range(len(scanners)):			
			if i1 == i2 : continue
			if not aligned_with_0[i1]: continue
			if     aligned_with_0[i2]: continue
			
			
			overlap, offset, rotation = figure_it_out(scanners[i1], scanners[i2])
			# if overlap:
			# 	print("Overlap found!")
			# continue

			if not overlap:
				# print("No overlap")
				continue

			print(f"\nIndex {i1} & {i2}")
			rotated_offset = rotation.dot(offset)
			to_0 = (offset + offset_to_0[i1]).astype(int)

			print(f"         offset: {offset}")
			print(f" rotated_offset: {rotated_offset}")
			print(f"    to_0 offset: {to_0}")
			print(np.sum(aligned_with_0))
			# Realign Scanner
			scanners[i2] = np.array([ rotation.dot(c) for c in scanners[i2] ])
			aligned_with_0[i2] = True
			rot_to_0[i2] = inv(rotation).dot(inv(rot_to_0[i1]))
			offset_to_0[i2] = to_0




#      offset: [  72. -168. 1125.]
# to_0 offset: [   52. -1301.  2186.]

#                 1105,-1205,1229 

# print("\n\n\n")

# all_locations = [ str(list(c)) for c in scanners[0] ]
all_locations = []
for i_scanner in range(len(scanners)):
	all_locations += [ str(list(c+offset_to_0[i_scanner])) for c in scanners[i_scanner] ]

print(len(list(set(all_locations))))

manhattan_distance = 0
for x in offset_to_0:
	for y in offset_to_0:
		distance = abs(x[0]-y[0]) + abs(x[1]-y[1]) + abs(x[2]-y[2])
		manhattan_distance = max(manhattan_distance, distance)
		print(distance)

print("Part 2:", manhattan_distance)


exit()

overlap, d1, r1 = figure_it_out(scanners[0], scanners[1])

if not overlap:
	exit()
print(d1)
print(r1)


# scanners1
print(scanners[0])

changed = scanners[1]
changed = scanners[1]
changed = np.array([ inv(r1).dot(s) for s in changed ])
# changed = scanners[1] - inv(r1).dot(d1)

# changed = inv(r1).dot(scanners[1].T).T
print(changed - d1)
# print(scanners[0])


exit()

d2, r2, d2_ = figure_it_out(scanners[1], scanners[4])

# -88, 113, 1104

print(r1)
print(r2)
print(r1*r2)
print(np.eye(3)*r1*r2)
print( (np.eye(3)*r1*r2).dot( d1 ))
print( (np.eye(3)*r1*r2).dot( d2 ))
print()

# print( inv(r1).dot(inv(r2).dot(d1)) )
# print( inv(r2).dot(inv(r1).dot(d1)) )

print( inv(r1).dot(inv(r2).dot(d2)) )

print(inv(r1).dot(inv(r2)))
print(inv(r1).dot(inv(r2)).dot(d2))



# print( inv(r2).dot(inv(r1).dot(d2)) )



exit()


for i_x, x in enumerate(X):
	print("\n\n\n==============")
	# xt = np.prod([x, T])
	xt = rotate(x)

	for i_y, y in enumerate(Y):
		# if i_x != i_y: continue

		# yt = np.prod([y, T])
		yt = rotate(y)
		yt = np.array([y])

		print(xt.shape)
		print("xt ", len(xt), p(xt))
		print("yt ", p(yt))	

		offsets = []
		for i_dx, dx in enumerate(xt):
			for i_dy, dy in enumerate(yt):
				offsets.append([list(dy-dx), dx])
		print(len(offsets))

		unique_offsets = np.unique(offsets, axis=0)

		# print(unique_offsets.shape)

		for offset, rot in unique_offsets:
			offset_str = str(list(offset))
			# print(offset_str)
			if offset_str not in coordinates: 
				coordinates[offset_str] = 0
				coordinates_rot[offset_str] = rot
			coordinates[offset_str] += 1

		# print(coordinates)

# for c in coordinates:
# 	print(coordinates[c], c)

coordinates_list = [ [v, k] for k, v in coordinates.items() if 12 <= v]
print(coordinates_list)

distance, string = coordinates_list[0]
print(string, coordinates_rot[string])

exit()

Xt = [ X*t for t in T ]
p(Xt)

for y in Y:
	XYd = [ x-y for x in Xt ]
	p(XYd)