power = {"A":1,"B":10,"C":100,"D":1000}

ABCD = "ABCD"
rooms = ["BA", "CD", "BC", "DA"]
spots = [" "*11]

rooms = ["AA", "..", "CC", "DD"]
spots = "BB........."

rooms = ["AD", "BB", "CC", "DA"]
spots = "BB........."

rooms = ["AB", "DC", "CB", "AD"]
spots = "..........."

spots_idx = [0,1,3,5,7,9,10]

# rooms = ["AA", "BB", "CC", "DD"]

def print_room(rooms, spots):
	string = "#############\n"
	string += "#" + spots + "#\n"
	string += "###" + "#".join([r[1] for r in rooms]) + "###\n"
	string += "  #" + "#".join([r[0] for r in rooms]) + "#  \n"
	string += "  #########  \n"
	print(string)

print_room(rooms, spots)

def is_free(pathway, _from, _to, allow_self=False):
	# print()
	# print("[is_free]", _from, _to, allow_self)
	
	if _from < _to: _to += 1
	if _to < _from: _from += 1
	# print("[is_free]", _from, _to, allow_self)
	if allow_self:
		if _from < _to: _from += 1
		if _to < _from: _from -= 1
	# print("[is_free]", _from, _to, allow_self)

	# print("[is_free]", pathway)
	c,d = sorted([_from, _to])
	r = list(range(c,d))

	# print("[is_free]", "".join([ "^" if x in r else "-" for x in range(len(pathway)) ]))

	pathway = pathway[c:d]
	# print("pathway", pathway)
	return pathway.count(".") == abs(c-d)

# print(is_free("...A...", 0, 2))
# print(is_free("...A...", 2, 0))
# print(is_free("...A...", 0, 3, allow_self=True))
# print(is_free("...A...", 3, 0, allow_self=True))
# exit()


def run(rooms, spots, total_power_consumed):
	rooms = rooms[:]
	spots = spots[:]
	
	l = lambda *args: print("[run]", *args)

	if rooms == ["AA", "BB", "CC", "DD"]:
		print("Done!")
		return total_power_consumed

	power_consumed = 0

	all_powers_consumed = [2**31] 

	# Check if X can move into correct room
	l("======== MOVING IN")
	for i in range(len(spots)):
		X = spots[i]
		if X == ".": continue

		room = ABCD.index(X)
		if rooms[room] != ".." and rooms[room] != X+".":
			# l(X, rooms[room], "Room unavailable")
			continue

		l("Room available for", X)

		room_entrance = (room+1)*2
		
		if not is_free(spots, i, room_entrance, allow_self=True): 
			l("Pathway blocked for", X)
			continue


		# Move X to room
		rooms_ = rooms[:]
		spots_ = spots[:]
		
		power_consumed = power[X]*abs(i-room_entrance)
		if rooms_[room] == X + ".":
			power_consumed += power[X]
			rooms_[room] = X+X
		if rooms_[room] == "..":
			power_consumed += power[X]*2
			rooms_[room] = X+"."
		spots_ = spots_[:i] + "." + spots_[i+1:]
		
		print("power_consumed", power_consumed)
		print_room(rooms_, spots_)

		all_powers_consumed += [run(rooms_, spots_, total_power_consumed + power_consumed)]


	l("======== MOVING OUT")
	# Check if X can move out of room
	for i_room, room in enumerate(rooms):
		if room == "..": continue
		if room == ABCD[i_room] + ".": continue
		if room == ABCD[i_room] + ABCD[i_room]: continue

		room_entrance = (i_room+1)*2
		
		room_idx = (room+".").index(".") - 1		
		X = room[room_idx]

		l(f"Considering moving {X} out from {room}")
		for spot in spots_idx:
			if not is_free(spots, room_entrance, spot): continue
			print(" Can move to", spot)

			spots_ = spots[:spot] + X + spots[spot+1:]
			rooms_ = rooms[:]
			rooms_[i_room] = room[::-1][room_idx]+"."
			power_consumed = 0	
			power_consumed += power[X] * (2-room_idx)
			power_consumed += power[X] * abs(room_entrance - spot)
			print("power_consumed", power_consumed)
			print_room(rooms_, spots_)

			all_powers_consumed += [run(rooms_, spots_, total_power_consumed + power_consumed)]

	print(all_powers_consumed)
	l("<=", min(all_powers_consumed))
	return min(all_powers_consumed)

run(rooms, spots, 0)








