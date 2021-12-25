# Part 1: 92967699949891, Part 2: 91411143612181

# Execute a single block of 18 instructions
def execute(memory, w, a, b, c):
	memory = { k : memory[k] for k in memory}
	memory['w'] = w
	memory['x'] = 1 * (memory['z'] % 26 + b != memory['w'])
	memory['z'] //= a
	memory['z'] *= 25*memory['x']+1
	memory['z'] += (memory['w']+c) * memory['x']
	return memory


# Parse instructions
instructions = open("input.txt").read().strip().split("\n")
instructions = [ [i[:3], i[4:]] for i in instructions ]
# Grab all unique inputs A, B, C
A, B, C = [], [], []
for i in range(0, len(instructions), 18):
	A.append( int(instructions[i:i+18][4 ][1].split(" ")[1]) )
	B.append( int(instructions[i:i+18][5 ][1].split(" ")[1]) )
	C.append( int(instructions[i:i+18][15][1].split(" ")[1]) )

# Create mapping between push and pop instructions
stack, map_push_pop = [], {}
for ia, a in enumerate(A):
	if a == 1: stack.append(ia)
	else:      
		ix = stack.pop()
		map_push_pop[ix] = ia
		map_push_pop[ia] = ix

def calculate(number):
	memory = {'w' : 0, 'x' : 0, 'y' : 0, 'z' : 0}
	index = 0

	while True and index < len(number):
		shrink = A[index] == 26

		previous_z = memory['z']
		memory_ = execute(memory, number[index], A[index], B[index], C[index])

		if shrink and not memory['z'] // 26 == memory_['z']:
			n = (previous_z % 26) + B[index]
			if n <= 0:      number[ map_push_pop[index] ] = number[ map_push_pop[index] ] - n + 1
			if 1 <= n <= 9: number[ index ] = n
			if 10 <= n:		number[ map_push_pop[index] ] = number[ map_push_pop[index] ] - n + 9
			memory = {'w' : 0, 'x' : 0, 'y' : 0, 'z' : 0}
			index = 0
			continue

		memory = memory_	
		index += 1
	return "".join([str(n) for n in number])

print("Part 1:", calculate( [9]*14 ))
print("Part 2:", calculate( [1]*14 ))