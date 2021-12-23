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

def is_free(pathway, _from, _to, allow_self=False):
	if _from < _to: _to += 1
	if _to < _from: _from += 1

	if allow_self:
		if _from < _to: _from += 1
		if _to < _from: _from -= 1

	c,d = sorted([_from, _to])
	r = list(range(c,d))

	pathway = pathway[c:d]
	return pathway.count(".") == abs(c-d)


@functools.cache
def run(rooms, spots, total_power_consumed, max_power=2**31, depth=0):
	rooms = eval(rooms)
	rooms = rooms[:]
	spots = spots[:]
	
	if max_power < total_power_consumed:
		return total_power_consumed, [[rooms, spots, 0]]

	finished = True
	for X, room in list(zip(ABCD, rooms)):
		finished = finished and room.count(X) == len(room)

	if finished:
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
			continue

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
		spots_ = spots[:i] + "." + spots[i+1:]

		power_consumed, state = run(str(rooms_), spots_, total_power_consumed + power_required, minimal_power_consumed, depth+1)
		if power_consumed < minimal_power_consumed:
			minimal_power_consumed = power_consumed
			minimal_state = state[:]
			minimal_state[-1] = power_required
			min_power_required = power_required

	# Check if X can move out of room
	for i_room, room in enumerate(rooms):
		# If room is empty or correctly filled, skip
		if room.count(".") + room.count(ABCD[i_room]) == len(room): 
			continue

		room_entrance = (i_room+1)*2
		X_idx = room.count(".")
		X = room[X_idx]

		for spot in spots_idx:
			if not is_free(spots, room_entrance, spot): continue

			spots_ = spots[:spot] + X + spots[spot+1:]
			rooms_ = rooms[:]
			room_ = room[:X_idx] + "." + room[X_idx+1:]
			rooms_[i_room] = room_
			
			power_required = 0	
			power_required += power[X] * (X_idx+1)
			power_required += power[X] * abs(room_entrance - spot)

			power_consumed, state = run(str(rooms_), spots_, total_power_consumed + power_required, minimal_power_consumed, depth+1)
			if power_consumed < minimal_power_consumed:
				minimal_power_consumed = power_consumed
				minimal_state = state[:]
				minimal_state[-1] = power_required
				min_power_required = power_required

	return minimal_power_consumed, [[rooms, spots, min_power_required]] + minimal_state


# my input 1
rooms = ["DD", "CA", "BA", "CB"]
spots = "..........."

minimal_power_consumed, states = run(str(rooms), spots, 0, 2**31)
print("Part 1:", minimal_power_consumed)


# my input 2
rooms = ["DDDD", "CCBA", "BBAA", "CACB"]
spots = "..........."

minimal_power_consumed, states = run(str(rooms), spots, 0, 2**31)
print("Part 2:", minimal_power_consumed)
