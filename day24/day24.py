instructions = open("input.txt").read().strip().split("\n")
instructions = [ [i[:3], i[4:]] for i in instructions ]

memory = {'w' : 0, 'x' : 0, 'y' : 0, 'z' : 0}

def print_memory(memory, a=None, b=None, c=None):
	print("          ", end="")
	for k in memory:
		print( (f"{k} : {memory[k]}" ).ljust(17), end="" )
	print()
	print("          ", end="")
	print( (f"{memory['z'] % 26}").ljust(6), end="")
	if a: print( (f"a={a}").ljust(6) , end="")
	if b: print( (f"b={b}").ljust(6) , end="")
	if c: print( (f"c={c}").ljust(6) , end="")
	# print()
	print()


def execute(memory, instruction, queue=[]):
	op, a_b = instruction
	a = a_b[0]
	b = a_b[2:] if 1 < len(a_b) else None

	if b and b in 'wxyz' : b = memory[b]
	if b : b = int(b)

	if op == "inp":
		if len(queue):
			memory[a] = queue.pop(0)
		else:
			print(f"$ {a} = ", end="")
			memory[a] = int(input())
	
	if op == "add" : memory[a] += b
	if op == "mul" : memory[a] *= b
	if op == "div" : memory[a] //= b
	if op == "mod" : memory[a] %= b
	if op == "eql" : memory[a] = int(memory[a] == b)

def execute_(memory, w, a, b, c):
	memstring = ", ".join([ (f"{k}={memory[k]}") for k in memory ])
	z = memory['z']
	go_down = a == 26

	print(f"[execute_]   {memstring.ljust(30)} z%={str(memory['z']%26).ljust(3)} w_in={w}, a={a}, b={b}, c={c}", end="")
	memory['w'] = w
	memory['x'] = 1 * (memory['z'] % 26 + b != memory['w'])
	memory['z'] //= a
	memory['z'] *= 25*memory['x']+1
	memory['z'] += (memory['w']+c) * memory['x']

	if go_down:
		expected_w = (z%26)+b
		print(f"   w should be { expected_w }    ", end="")
		if w != expected_w: 
			print()
			return False

	print(f"          {z} => {memory['z']}")
	return True

def run(memory_, instructions_, queue_, A, B, C):
	memory = { k : memory_[k] for k in memory_}
	instructions = instructions_[:]
	queue = queue_[:]
	
	i_instr = 0
	# while len(instructions):
	works = False
	while len(A):
		a,b,c = A.pop(0), B.pop(0), C.pop(0)
		works = execute_(memory, queue.pop(0), a, b, c)
		if not works: break
	if works:
		print("DONE!!!!")
		print(queue_)
		exit()

	# while len(instructions):
		# if(instructions[0][0] == "inp"):
		# 	# execute(memory, instructions.pop(0), queue)
		# 	execute_(memory, instructions.pop(0), queue.pop(0), a, b, c)
		# 	print_memory(memory, A[i_instr], B[i_instr], C[i_instr])
		# 	i_instr += 1
		# else:
		# 	execute(memory, instructions.pop(0), queue)
		# 	execute_(memory, instructions.pop(0), queue.pop(0), a, b, c)
	# return memory
	return works


sets = []
for i in range(18): sets.append([])
for i in range(0, len(instructions), 18):
	subs = instructions[i:i+18]
	for isub, sub in enumerate(subs):
		string_sub = " ".join(sub)
		# if string_sub not in sets[isub]:
		sets[isub].append(string_sub)
# for s in sets:
# 	if len(s) == 1: continue
# 	print("|".join([ s_.ljust(9) for s_ in s ]))
print("|".join([ s_.ljust(9) for s_ in sets[4] ]))
print("|".join([ s_.ljust(9) for s_ in sets[5] ]))
print("|".join([ s_.ljust(9) for s_ in sets[15]]))

# for s in sets[4]:
# 	s.split(" ")[-1]
A = [ int(s.split(" ")[-1]) for s in sets[4]  ]
B = [ int(s.split(" ")[-1]) for s in sets[5]  ]
C = [ int(s.split(" ")[-1]) for s in sets[15] ]

queue = [1,3,5,7,9,2,4,6,8,9,9,9,9,9]

#       [ 1, 1, 1,26, 1, 1,26,26, 1,26, 1,26,26,26]
queue = [ 9, 2, 9, 6, 7, 6, 9, 9, 9, 4, 9, 8, 9, 1]
# 92967699948791 too low
# 92967699949891

#       [ 1, 1, 1,26, 1, 1,26,26, 1,26, 1,26,26,26]
queue = [ 9, 1, 5, 2, 1, 1, 4, 3, 6, 1, 2, 1, 8, 1]
print("".join([str(q) for q in queue]))
run(memory, instructions, queue, A[:], B[:], C[:])

exit()

# Too low 11411143612111
# Too low 21111111111111
# Too low 61111111111111
# 91521143612181 done
zs = []


integer = 92967699949893
queue = [ int(x) for x in list(str(integer)) ]
print(queue)

while True:
	it_works = run(memory, instructions, queue, A[:], B[:], C[:])
	if not it_works:
		integer -= 1
		queue = [ int(x) for x in list(str(integer)) ]

# print_memory(mem)

# The digit 0 cannot appear in a model number.

# if a=1, push w+c in base 26
#https://www.reddit.com/user/etotheipi1
#https://www.reddit.com/r/adventofcode/comments/rnejv5/2021_day_24_solutions/hps5hgw/?context=3
# else if a=26, then pop
exit()

w = int(input())
x = int((z % 26) + b != w)

if a == 1: # then x is always 1. 10 <= B
	z *= 26
	z += (w+c)

if a == 26: # then x is ?. B <= 0
	# if x = 0 then just pop happens
	# if x = 1 push also happens
	z //= 26
	z *= 25*x+1
	z += (w+c)*x


z *= 25*x+1 
## int((z % 26) + b != w) must be 1
## z % 26 = w'+c from previous
#### w'+c+b != w : w'+c != w-b
