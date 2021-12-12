lines = open("input.txt").read().splitlines()

connections = {}
for line in lines:
	a, b = line.split("-")
	if a not in connections: connections[a] = []
	if b not in connections: connections[b] = []

	connections[a].append(b)
	connections[b].append(a)

def walk(connections, path, visited, visited_twice=False):
	at = path[-1]
	if at == 'end': return [path]

	options = connections[at]
	options = [ o for o in options if (o not in visited or o.isupper() or not visited_twice) and o != 'start' ]
	
	return_paths = []
	for option in options:
		next_paths = walk(connections, path + [option], visited + [at], visited_twice or option in visited and option.islower())
		for next_path in next_paths: return_paths.append(next_path)

	return return_paths

paths = walk(connections, ['start'], [], True)
print("Part 1 :", len(paths))

paths = walk(connections, ['start'], [], False)
print("Part 2 :", len(paths))