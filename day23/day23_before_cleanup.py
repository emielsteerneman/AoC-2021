import functools

power = {"A":1,"B":10,"C":100,"D":1000}

ABCD = "ABCD"

# example input 1
rooms = ["BA", "CD", "BC", "DA"]
spots = "..........."

# example input 2
rooms = ["BDDA", "CCBD", "BBAC", "DACA"]
spots = "..........."

# my input 1
# rooms = ["DD", "CA", "BA", "CB"]
# spots = "..........."

# my input 2
rooms = ["DDDD", "CCBA", "BBAA", "CACB"]
spots = "..........."


spots_idx = [0,1,3,5,7,9,10]

spots_idx = [3,5,7,9,1,10,0]

# rooms = ["AA", "BB", "CC", "DD"]

def print_room(rooms, spots, depth=0):
	# string = "#############\n"
	string =""
	string += "    " * depth + "#" + spots + "#\n"
	for i_r in range(len(rooms[0])):
		# string += "    " * depth + "###" + "#".join([r[1] for r in rooms]) + "###\n"
		string += "    " * depth + "|  " + " ".join([r[i_r] for r in rooms]) + "  |\n"
	# string += "  #########  \n"
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

@functools.cache
def run(rooms, spots, total_power_consumed, max_power=2**31, depth=0):
	rooms = eval(rooms)
	rooms = rooms[:]
	spots = spots[:]
	
	l = lambda *args: print("    "*depth + "[run]", *args)
	l(rooms, spots, total_power_consumed, max_power)
	print_room(rooms, spots, depth)

	if max_power < total_power_consumed:
		l(f"Killed! {max_power} < {total_power_consumed}")
		return total_power_consumed, [[rooms, spots, 0]]

	finished = True
	for X, room in list(zip(ABCD, rooms)):
		finished = finished and room.count(X) == len(room)

	if finished:
		l(f"Done! total_power_consumed={total_power_consumed} max_power={max_power}")
		return total_power_consumed, [[rooms, spots, 0]]

	minimal_power_consumed = max_power
	minimal_state = [[rooms, spots]] 
	min_power_required = 0




	moved_in = False

	# Check if X can move into correct room
	for i in range(len(spots)):
		X = spots[i]
		if X == ".": continue
		room_idx = ABCD.index(X)
		room = rooms[room_idx][:]
		
		# Check if X can move into room by checking if any !X is in it
		if room.count(X) + room.count(".") != len(room):
			l(f"[in] Can't move {X} into room {room}")
			continue
		l(f"[in] Trying to move {X} into room {room_idx}:{room}")

		room_entrance = (room_idx+1)*2
		
		if not is_free(spots, i, room_entrance, allow_self=True):
			continue

		moved_in = True

		# Move X to room
		rooms_ = rooms[:]
		spots_ = spots[:]
				
		power_required  = power[X] * abs(i-room_entrance)
		power_required += power[X] * room.count(".")
		
		room_ = ("." * (room.count(".")-1) + X * len(room) )[:len(room)]
		rooms_[room_idx] = room_
		# print(room, "=>", room_)

		spots_ = spots[:i] + "." + spots[i+1:]
		# print(spots, "=>", spots_)


		power_consumed, state = run(str(rooms_), spots_, total_power_consumed + power_required, minimal_power_consumed, depth+1)
		if power_consumed < minimal_power_consumed:
			l(f"!! Found new lowest power {power_consumed}")
			minimal_power_consumed = power_consumed
			minimal_state = state[:]
			minimal_state[-1] = power_required
			min_power_required = power_required

	if moved_in:
		minimal_power_consumed, [[rooms, spots, ]] + minimal_state

	# Check if X can move out of room
	for i_room, room in enumerate(rooms):
		# If room is empty or correctly filled, skip
		if room.count(".") + room.count(ABCD[i_room]) == len(room): 
			# l(f"[out] Room {i_room}:{room} empty")
			continue
		# if room[room.count(".")] == ABCD[i_room]:
		# 	c = room.count(".")
		# 	# l(f"[out] Room {i_room}:{room}[{c}] = {room[c]} already correct")
		# 	continue

		room_entrance = (i_room+1)*2
		X_idx = room.count(".")
		X = room[X_idx]

		l(f"[out] Moving {X_idx}:{X} out of {i_room}:{room}")

		for spot in spots_idx:
			if not is_free(spots, room_entrance, spot): continue

			# l(f"[out]  Moving {X} to {spot}")
			spots_ = spots[:spot] + X + spots[spot+1:]
			rooms_ = rooms[:]
			room_ = room[:X_idx] + "." + room[X_idx+1:]
			# print(rooms_)
			rooms_[i_room] = room_
			
			# l("[out] ", room, "=>", room_)
			# l("[out] ", spots, "=>", spots_)
			# print(rooms_)
			# exit()
			power_required = 0	
			power_required += power[X] * (X_idx+1)
			power_required += power[X] * abs(room_entrance - spot)

			# l("power_required", power_required)
			# print_room(rooms_, spots_, depth)

			power_consumed, state = run(str(rooms_), spots_, total_power_consumed + power_required, minimal_power_consumed, depth+1)
			if power_consumed < minimal_power_consumed:
				l(f"!! Found new lowest power {power_consumed}")
				minimal_power_consumed = power_consumed
				minimal_state = state[:]
				minimal_state[-1] = power_required
				min_power_required = power_required

	l("<=", minimal_power_consumed)
	return minimal_power_consumed, [[rooms, spots, min_power_required]] + minimal_state


# run(str(["BA", "CD", "BC", "DA"]), "...........", 0, 2**30)
# exit()
minimal_power_consumed, states = run(str(rooms), spots, 0, 2**31)

print("\n\n\n\n")

for rooms, spots, power_required in states:
	print_room(rooms, spots)
	print(power_required)








