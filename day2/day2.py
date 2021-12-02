commands = open("input1.txt").read().strip().split("\n")

# Part 1
hor, ver = 0, 0

for command in commands:
	action, value = command.split(" ")
	if action == "forward": hor += int(value)
	if action == "down": ver += int(value)
	if action == "up": ver -= int(value)

print(hor * ver)

hor, ver, aim = 0, 0, 0

for command in commands:
	action, value = command.split(" ")
	if action == "forward": 
		hor += int(value)
		ver += int(value) * aim
	if action == "down": aim += int(value)
	if action == "up": aim -= int(value)

print(hor * ver)