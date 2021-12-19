import numpy as np
import itertools
import re

## Create all rotational matrices. This is such a hack... 
# Literally generate all possible matrices, and filter for valid rotational ones.
# It's valid if det(M) == 1 and M.T == M^-1. No idea why, but Google says so.
# There should be a total of 24 rotational matrices. Again, Google.
R = list(itertools.product([-1, 0, 1], repeat=9))
R = [np.array(r).reshape((3, 3)) for r in R]
R = [ m for m in R if np.linalg.det(m) == 1 ]
R = [ m for m in R if ( m.T == np.linalg.inv(m) ).all() ]

def get_input():
	file = open("input.txt").read().replace("\n\n", "\n").strip()
	scanners_string = re.split(r"---.*---\n", file)[1:]
	scanners_string = [ scanner.strip().split("\n") for scanner in scanners_string]

	scanners = []

	for scanner_string in scanners_string:
		scanner = np.array([ list(map(int, line.split(","))) for line in scanner_string ])
		scanners.append(scanner)

	return np.array(scanners)

def find_overlap(X, Y):
	distances = {}
	# Get the distance between all elements of x and all elements of y, while rotating y in all possible configurations
	for i_x, x in enumerate(X):
		for i_y, y in enumerate(Y):
			for i_r, r in enumerate(R):
				distance = x - r.dot(y)		# Rotate y and get distance to x
				s = str(distance)			# Use string as dict key
				if s not in distances: 		# Initialize to [0, rotation, distance] if needed
					distances[s] = [0, r, distance] 
				distances[s][0] += 1 		# Increase count of distance by 1

	# An overlap is only valid if it occurs exactly 12 times
	overlaps = [ v for k, v in distances.items() if 12 == v[0] ]

	# No overlaps found
	if len(overlaps) == 0: 
		return False, None, None

	# Overlap found, return distance and rotational matrix
	count, rotation, distance = overlaps[0]
	return True, distance, rotation



# Get input
scanners = get_input()
# List that keeps track of which scanner are aligned with scanner 0
# scanner 0 is of course aligned with itself
aligned_with_0 = [True] + [False] * (len(scanners) - 1)
# List that keeps track of the distances each scanner and scanner 0
# scanner 0 has of course a distance of [0,0,0] to itself
distances_to_0 = [np.zeros(3, dtype=int)] + [None] * (len(scanners) - 1)

# While there are still unaligned scanner
while False in aligned_with_0:
	# For each scanner combination
	for i1 in range(len(scanners)):
		for i2 in range(len(scanners)):			
			if i1 == i2 : continue				# Don't compare scanner with itself
			if not aligned_with_0[i1]: continue # Don't use an unaligned scanner as reference
			if     aligned_with_0[i2]: continue # Don't align a scanner that is already aligned
			
			# Check for overlap between two scanners
			overlap, offset, rotation = find_overlap(scanners[i1], scanners[i2])
			# Continue if there is no overlap
			if not overlap: continue

			# Calculate distance to scanner 0
			distance_to_0 = (offset + distances_to_0[i1]).astype(int)

			# Realign scanner to 0
			scanners[i2] = np.array([ rotation.dot(c) for c in scanners[i2] ])
			aligned_with_0[i2] = True			# Set aligned to True
			distances_to_0[i2] = distance_to_0 	# Store distance to scanner 0

# Find all locations by adding to each scanner its offset and storing the locations as string
all_locations = []
for i_scanner in range(len(scanners)):
	all_locations += [ str(list(c + distances_to_0[i_scanner])) for c in scanners[i_scanner] ]
# Filter out duplicate locations and print the length
print("Part 1:", len(list(set(all_locations))))

# Find largest manhattan distance
manhattan_distance = 0
for x in distances_to_0:
	for y in distances_to_0:
		distance = abs(x[0]-y[0]) + abs(x[1]-y[1]) + abs(x[2]-y[2])
		manhattan_distance = max(manhattan_distance, distance)
print("Part 2:", manhattan_distance)