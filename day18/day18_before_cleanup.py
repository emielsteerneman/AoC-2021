import json
# input_list = [  [  [  [  [9,8],1  ],2  ],3  ],4  ]
# input_list = [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]
input_list = [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]


is_int  = lambda x : type(x) == int
is_list = lambda x : type(x) == list

def print_tree(values):

	all_paths = [ v[0] for v in values]

	max_length = max([ len(p) for p in all_paths])
	width = 2**(max_length+1)

	paths = []
	for e in range(max_length-1):
		for i in range(2**(e+1)):
			new_path = "{0:b}".format(i).rjust(e+1,"0")
			if len([ p for p in all_paths if p.startswith(new_path)]):
				paths.append(new_path)

	nodes, n = [], 0
	for p in sorted(paths):
		nodes.append([p, n])
		n += 1

	def get_x(string): 
		total = width//2
		for i_char, char in enumerate(string):
			offset = 2**(max_length-i_char-1)
			total_ = total - offset if char == "0" else total + offset
			# print(f"  gx {string} i={i_char} offset={offset} total={total} => {total_}")
			total = total_
			
		return total*2
	get_y = lambda string : len(string)



	n_rows = max([ len(v[0]) for v in values]) + 1

	text = ["-" * width*2] * (n_rows*2)

	for path, _ in nodes:
		x, y = get_x(path), get_y(path)*2
		val_str = "█"
		dx1, dx2 = len(val_str)//2, len(val_str)-len(val_str)//2
		text[y] = text[y][:x-dx1] + val_str + text[y][x+dx2:]

	for path, val in values:
		x, y = get_x(path), get_y(path)*2
		val_str = str(val)
		dx1, dx2 = len(val_str)//2, len(val_str)-len(val_str)//2
		text[y] = text[y][:x-dx1] + val_str + text[y][x+dx2:]

	print("\n".join(text))

class Node:
	def __init__(self, pairs, path=""):
		# print("New Node", pairs, path)

		self.path = path
		self.is_int = is_int(pairs)

		self.l = lambda *args : print("  "*len(self.path), f"[Node {self.path}]" if not self.is_int else f"[Leaf {self.path} ({self.value})]", *args)

		if self.is_int:
			self.value = pairs
		else:
			left, right = pairs

			if is_list(left) or is_int(left): left = Node(pairs[0], path + "0")
			else: left.increment_path("0")
			self.node_left = left

			if is_list(right) or is_int(right): right = Node(pairs[1], path + "1")
			else: right.increment_path("1")
			self.node_right = right

	def get(self):
		if self.is_int: result = [[self.path, self.value]]
		else:			result = self.node_left.get() + self.node_right.get()
		return result

	def get_magnitude(self):
		if self.is_int: return self.value
		return 3 * self.node_left.get_magnitude() + 2 * self.node_right.get_magnitude()

	def update(self):
		print("[update]")
		while True:
			print("\n\n[update] Next iteration")
			change_outer = False
			
			while True:
				change_explode = self.start_explode()
				change_outer = change_outer or change_explode
				if not change_explode: break
				print_tree(self.get())
			print("[update] Exploding done")
			
			# print(self.get())
			change_split = self.do_split()
			change_outer = change_outer or change_split
			if change_split:
				print_tree(self.get())
			print("Splitting done")
			
			if not change_outer: break

		print("[update] complete")

	def do_split(self):
		if self.is_int: return False

		if self.node_left.is_int and 10 <= self.node_left.value:
			val = self.node_left.value
			x, y = val // 2, val - val // 2
			self.l(f"Splitting left into {x} and {y}")
			self.node_left = Node([x, y], self.path + "0")

			print_tree(self.get())

			return True

		if self.node_left.do_split() : return True
		
		if self.node_right.is_int and 10 <= self.node_right.value:
			val = self.node_right.value
			x, y = val // 2, val - val // 2
			self.l(f"Splitting right into {x} and {y}")
			self.node_right = Node([x, y], self.path + "1")
			return True
		
		if self.node_right.do_split(): return True

		return False

	def start_explode(self):
		state = self.get()
		result, [left, right] = self.do_explode()
		if result:
			# print("Explosion found!", left, right)
			# print(state)
			to_left, to_right = state.index(left)-1, state.index(right)+1
			if 0 <= to_left: 
				# print("Adding left to", state[to_left])
				self.add(state[to_left][0], left[1])
			if to_right < len(state) : 
				# print("Adding right to", state[to_right])
				self.add(state[to_right][0], right[1])
		return result

	def do_explode(self, depth=0):

		if self.node_left.is_int and self.node_right.is_int and 4 <= depth:
			x, y = self.node_left.value, self.node_right.value

			self.is_int = True
			self.value = 0

			result = [[self.node_left.path,self.node_left.value], [self.node_right.path, self.node_right.value]]

			self.l("Explode :", result)

			return True, result

		else:
			if not self.node_left.is_int:
				result = explode_found, [left, right] = self.node_left.do_explode(depth+1)
				if explode_found: return result

			if not self.node_right.is_int:
				result = explode_found, [left, right] = self.node_right.do_explode(depth+1)
				if explode_found: return result

		return False, [None, None]

	def add(self, path, val):
		if self.is_int:
			self.l("Adding value", self.value, "=>", val+self.value)
			self.value += val
		else:
			next_node = self.node_left if path[0] == "0" else self.node_right
			# self.l("add", "path=", path, ", next_node =", next_node.path)
			next_node.add(path[1:], val)
			# if path.startswith(self.node_left.path): self.node_left.add(path, val)
			# if path.startswith(self.node_right.path): self.node_right.add(path, val)

	def add_right(self, val):
		if self.is_int: 
			self.l(f"Added {val}")
			self.value += val
		else: self.node_right.add_right(val)
	
	def add_left(self, val):
		if self.is_int: 
			self.value += val
			self.l(f"Added {val}")
		else: self.node_left.add_left(val)

	def increment_path(self, dpath):
		# print("[increment_path]", self.path, "=>", dpath + self.path)
		self.path = dpath + self.path
		if self.is_int: return

		self.node_left.increment_path(dpath)
		self.node_right.increment_path(dpath)

# inputs = open("input.txt").read().split("\n")
# start, *inputs = [ json.loads(i) for i in inputs ]
# tree = Node(start)
# tree.update()
# print_tree(tree.get())

# for i in inputs:
# 	print(i)
# 	tree = Node([tree, i])
# 	print_tree(tree.get())
# 	tree.update()
# 	print_tree(tree.get())
# print(tree.get())

# print("Magnitude:", tree.get_magnitude())









inputs = open("input.txt").read().split("\n")
inputs = [ json.loads(i) for i in inputs ]

lowest = 0


for i1, l1 in enumerate(inputs):
	for i2, l2 in enumerate(inputs):
		if i1 == i2: continue
		print(l1, l2)
		tree = Node([l1, l2])
		tree.update()
		lowest = max(lowest, tree.get_magnitude())


print(lowest)

exit()





start, *inputs = [ json.loads(i) for i in inputs ]
tree = Node(start)
tree.update()
print_tree(tree.get())

for i in inputs:
	print(i)
	tree = Node([tree, i])
	print_tree(tree.get())
	tree.update()
	print_tree(tree.get())
print(tree.get())

print("Magnitude:", tree.get_magnitude())



















exit()




# input_list = [ [15, 3], [19, [12, 3]] ]

tree = Node(input_list)

print_tree(tree.get())

while True:
	change_outer = False
	while True:
		change_split = tree.do_split()
		change_outer = change_outer or change_split
		if not change_split: break
	while True:
		change_explode = tree.start_explode()
		change_outer = change_outer or change_explode
		if not change_explode: break
	if not change_outer: break

print_tree(tree.get())



















exit()



print_tree(tree.get())

print("\nExplode")
tree.start_explode()	

print_tree(tree.get())

tree.start_explode()

print_tree(tree.get())

tree.do_split()

print_tree(tree.get())

tree.do_split()

print_tree(tree.get())

tree.start_explode()

print_tree(tree.get())

# while True:
# 	print_tree(tree.get())
# 	if not tree.do_split():
# 		break

exit()


def create_this_weird_tree(tree, path="", depth=0):
	l = lambda *args : print("  "*depth, "[ctwt]", *args)
	
	if is_int(tree): 
		l("END", path, tree)
		return [[path, tree]]

	l(tree[0], "    |    ", tree[1])

	left, right = tree

	result_left = create_this_weird_tree(left, path+"0", depth+1)
	# l("RL", result_left)
	# for i in range(len(result_left)):
	# 	result_left[i][0] = "0" + result_left[i][0]

	result_right = create_this_weird_tree(right, path+"1", depth+1)
	# l("RL", result_left)
	# for i in range(len(result_right)):
	# 	result_right[i][0] = "1" + result_right[i][0]

	result = result_left + result_right
	l(result)

	return result

output = create_this_weird_tree(input_list)
print(output)
print(sorted(output))

exit()

def walk(lst, depth=0, outer_left=None, outer_right=None):
	l = lambda *args : print("  "*depth, *args)

	if depth == 4: print("Explode")

	left, right = lst

	next_left  = left  if is_int(left)  else outer_left
	next_right = right if is_int(right) else outer_right
	
	l("L:",left,"R:",right, "nl", next_left, "nr", next_right)

	if not is_int(left):
		inner_left, inner_right = walk(left , depth+1, next_left, next_right)
		l("inner_left", inner_left, "inner_right", inner_right)
	else:
		l(f"SUM {left} with {outer_left} and {right} with {outer_right}" )	




	if not is_int(right):
		inner_left, inner_right = walk(right, depth+1, next_left, next_right)

	return left, right

	# left, right = None, None
	# for i_sub, sub in enumerate(lst): 
	# 	l("Left", get_left(i_sub, lst))
	# 	l("Right", get_right(i_sub, lst))
	# 	walk(sub, depth+1)

		

walk(input_list)