file = open("input.txt").read().strip().splitlines()

in_out = []
for line in file:
	in_, out = line.split(" | ")
	in_ = [ ''.join(sorted(s.strip())) for s in in_.upper().split(" ") ]
	out = [ ''.join(sorted(s.strip())) for s in out.upper().split(" ") ]
	in_out.append([in_, out])

counter = sum([ len(digit) in [2, 3, 4, 7] for _,out in in_out for digit in out ])
print("Part 1 :", counter)

number_to_segments = [
	"abcefg", # 0
	"cf",     # 1
	"acdeg",  # 2
	"acdfg",  # 3
	"bcdf",   # 4
	"abdfg",  # 5
	"abdefg", # 6
	"acf",    # 7
	"abcdefg",# 8
	"abcdfg"  # 9
]

# List/String operations
subtract  = lambda a, b : list(set([ x for x in a if x not in b ]))
intersect = lambda lists: ''.join(sorted(set.intersection(*map(set,lists))))
union     = lambda lists: ''.join(sorted(set().union(*lists)))

def figure_it_out(inn, out):
	mapping = { c : "ABCDEFG" for c in "abcdefg" }

	# Create mapping
	for input_segments in inn:
		# Get all possible segments based on number of enabled segments and number-to-segment mapping
		possible_segments = [segments for segments in number_to_segments if len(segments) == len(input_segments)]

		# Segments present in all possible segments
		included_segments = intersect(possible_segments)
		# Segments not present in any possible segment
		excluded_segments = subtract("abcdefg", union(possible_segments))

		# For all included segments, get intersection between previously extrapolated segments and newly given segments
		for segment in included_segments: mapping[segment] = intersect([mapping[segment], input_segments])
		# For all excluded segments, remove newly given segments from previously extrapolated segments
		for segment in excluded_segments: mapping[segment] = subtract(mapping[segment], input_segments)

	# Solve mappings that have more than one connection
	for segment, connections in mapping.items():
		# Only consider solved segment mappings
		if len(connections) != 1: continue 
		for segment_, connections_ in mapping.items():
			# Skip self
			if segment_ == segment: continue
			# Subtract solved segment mapping from all other possible mappings
			mapping[segment_] = subtract(connections_, connections)

	# Create new number-to-segments mapping
	number_to_segments_ = []
	for number, segments in enumerate(number_to_segments):
		new_segments = ''.join(sorted([ mapping[char][0] for char in segments ]))
		number_to_segments_.append(new_segments)

	# Calculate numbers and total value
	numbers = [ number_to_segments_.index(segments) for segments in out ]
	total = numbers[0]*1000 + numbers[1]*100 + numbers[2]*10 + numbers[3]
	return total

print("Part 2 :", sum([ figure_it_out(inn, out) for inn, out in in_out ]))