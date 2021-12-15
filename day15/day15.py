import numpy as np 
cave_txt = open("input.txt").read().split("\n")

# Create cave
H, W = len(cave_txt), len(cave_txt[0])
cave = np.array([ int(c) for c in "".join(cave_txt) ], dtype=np.uint8).reshape((H, W))

# Create mega cave
megacave = np.zeros((H*5, W*5), dtype=np.uint8)
for y in range(5):
	for x in range(5):
		index = np.s_[y*H:(y+1)*H, x*W:(x+1)*W,]
		megacave[index] = (cave - 1 + x + y) % 9
megacave += 1

is_in = lambda x, y, W, H : 0 <= x < W and 0 <= y < H

def solve_cave(cave):
	H, W = cave.shape

	cost_map = np.ones((H, W)) * np.inf
	update_map = np.ones((H, W), dtype=bool)
	
	cave[0, 0] = 0
	cost_map[0, 0] = cave[0, 0]

	n_iterations = 1
	while 0 < np.sum(update_map):
		n_iterations += 1

		for (y, x), risk in np.ndenumerate(cave):
			if not update_map[y, x] : continue

			cost = cost_map[y, x]
			risk = cave[y, x]

			update_surrounding = False

			offsets = [[0,1],[1,0],[0,-1],[-1,0]]

			for dx, dy in offsets:
				sx, sy = x+dx, y+dy
				if is_in(sx, sy, W, H):
					if cost_map[sy, sx] + risk < cost:
						cost_map[y, x] = cost_map[sy, sx] + risk
						update_surrounding = True

			if update_surrounding:
				for dx, dy in offsets:
					sx, sy = x+dx, y+dy
					if is_in(sx, sy, W, H):
						update_map[sy, sx] = True

			update_map[y, x] = False

	return cost_map[H-1, W-1]

print("Part 1 :", solve_cave(cave))
print("Part 2 :", solve_cave(megacave))
