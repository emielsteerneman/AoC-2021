import functools

dice = 0

p1_pos = 4
p2_pos = 8

p1_score = 0
p2_score = 0

while True:
	total = (dice+2)*3
	dice += 3

	p1_pos = (p1_pos-1 + total) % 10 + 1
	p1_score += p1_pos

	total = (dice+2)*3
	dice += 3

	p2_pos = (p2_pos-1 + total) % 10 + 1
	p2_score += p2_pos

	if 1000 <= p1_score:
		print("Part 1:", p2_score * dice)
		break

	if 1000 <= p2_score:
		print("Part 1:", p1_score * dice)
		break


dice_counts = [0]*10
for a in [1,2,3]:
	for b in [1,2,3]:
		for c in [1,2,3]:
			dice_counts[a+b+c] += 1


step = lambda p, s : (p-1 + s) % 10 + 1

@functools.cache
def throw(p1, s1, p2, s2, i=0):

	if 21 <= s1: return [1, 0]
	if 21 <= s2: return [0, 1]

	wins = [0, 0]

	if i % 2 == 0:
		for d, dc in enumerate(dice_counts):
			if dc == 0: continue
			pos_next = step(p1, d)
			wins_p1, wins_p2 = throw(pos_next, s1+pos_next, p2, s2, i+1)
		
			wins[0] += wins_p1 * dc
			wins[1] += wins_p2 * dc
	else:
		for d, dc in enumerate(dice_counts):
			if dc == 0: continue
			pos_next = step(p2, d)
			wins_p1, wins_p2 = throw(p1, s1, pos_next, s2+pos_next, i+1)
		
			wins[0] += wins_p1 * dc
			wins[1] += wins_p2 * dc

	return wins

wins = throw(8,0,2,0)
print("Part 2:", max(wins))