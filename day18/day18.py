import json

is_int  = lambda x : type(x) == int
is_list = lambda x : type(x) == list

class Node:
	def __init__(self, pairs, path=""):

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
		# Keep updating while either an explosion or split happened
		while True:
			change_occured = False
			# Explode as much as possible
			while True:
				change_explode = self.start_explode()
				change_occured = change_occured or change_explode
				if not change_explode: break			
			# Split only once, then try to explode again
			change_split = self.do_split()
			change_occured = change_occured or change_split
			# Stop if neither an explode or split occured
			if not change_occured: break

	def do_split(self):
		if self.is_int: return False

		# Split left Leaf into two Nodes if needed
		if self.node_left.is_int and 10 <= self.node_left.value:
			value = self.node_left.value
			left, right = value // 2, value - value // 2
			self.node_left = Node([left, right], self.path + "0")
			return True
		
		# Search for a split in the left Node
		if self.node_left.do_split() : return True
		
		# Split right Leaf into two Nodes if needed
		if self.node_right.is_int and 10 <= self.node_right.value:
			value = self.node_right.value
			left, right = value // 2, value - value // 2
			self.node_right = Node([left, right], self.path + "1")
			return True
		
		# Search for a split in the right Node
		if self.node_right.do_split(): return True

		# Didn't find a split in any sub-Nodes
		return False

	def start_explode(self):
		state = self.get()
		explode_found, [left, right] = self.do_explode()
		
		if not explode_found: return False
		
		# Find Leafs to the left and right of the exploded Leafs
		to_left, to_right = state.index(left)-1, state.index(right)+1
		# Increment left Leaf if it exists
		if 0        <= to_left    : self.add(state[to_left][0], left[1])
		# Increment right Leaf if it exists
		if to_right <  len(state) : self.add(state[to_right][0], right[1])
		
		return True

	def do_explode(self, depth=0):
		# If both sub-Nodes are Leaves, and this Node deep enough
		if self.node_left.is_int and self.node_right.is_int and 4 <= depth:
			# Convert from Node to Leaf
			self.is_int = True
			self.value = 0
			# Return Leafs
			return True, [[self.node_left.path, self.node_left.value], [self.node_right.path, self.node_right.value]]

		else:
			# If left is not a Leaf, search there for something to explode
			if not self.node_left.is_int:
				result = explode_found, [left, right] = self.node_left.do_explode(depth+1)
				if explode_found: return result
			
			# If right is not a Leaf, search there for something to explode
			if not self.node_right.is_int:
				result = explode_found, [left, right] = self.node_right.do_explode(depth+1)
				if explode_found: return result

		# No explosion found in either sub-Nodes
		return False, [None, None]

	def add(self, path, val):
		if self.is_int:
			self.value += val
		else:
			next_node = self.node_left if path[0] == "0" else self.node_right
			next_node.add(path[1:], val)

	def increment_path(self, dpath):
		self.path = dpath + self.path
		if self.is_int: return

		self.node_left.increment_path(dpath)
		self.node_right.increment_path(dpath)

### Part 1
inputs = open("input.txt").read().split("\n")
start, *inputs = [ json.loads(i) for i in inputs ]

tree = Node(start)
tree.update()

for i in inputs:
	tree = Node([tree, i])
	tree.update()
print("Part 1:", tree.get_magnitude())

### Part 2
inputs = open("input.txt").read().split("\n")
inputs = [ json.loads(i) for i in inputs ]

highest_magnitude = 0

for i1, l1 in enumerate(inputs):
	for i2, l2 in enumerate(inputs):
		if i1 == i2: continue
		tree = Node([l1, l2])
		tree.update()
		highest_magnitude = max(highest_magnitude, tree.get_magnitude())

print("Part 2:", highest_magnitude)
