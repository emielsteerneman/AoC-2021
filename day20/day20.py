import numpy as np

def print_image(image):
	for line in image:
		print( "".join([".#"[c] for c in line ] ))

file = open("input.txt").read().strip().split("\n")

IEA = file.pop(0)
file.pop(0)

width, height = len(file[0]), len(file)
image = np.zeros((height, width), dtype=bool)

for i_line, line in enumerate(file):
	for i_char, char in enumerate(line):
		image[i_line, i_char] = char == "#"

for i in range(50):
	image = np.pad(image, pad_width=1, constant_values= i%2==1 )

	outer_image = np.pad(image, pad_width=1, constant_values= i%2==1 )
	image = outer_image[1:-1, 1:-1]

	height, width = image.shape
	image_new = np.zeros(image.shape, dtype=bool)
	for y in range(0, height):
		for x in range(0, width):
			sub_image = outer_image[y:y+3, x:x+3]
			string = sub_image.flatten()
			string = "".join([ "0" if not c else "1" for c in string ])
			index = int(string, 2)
			image_new[y, x] = IEA[index] == "#"

	image = image_new

	if i == 1:
		print("Part 1:", np.sum(image))
	if i == 49:
		print("Part 2:", np.sum(image))