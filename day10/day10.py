import functools
import re

chars_open = "({[<"
chars_close= ")}]>"

open_to_close = { "(":")", "[":"]", "{":"}", "<":">" }
error_score = {")":3, "]":57, "}":1197, ">":25137}
autocomplete_score = {")":1, "]":2, "}":3, ">":4}



lines = open("input.txt").read().strip().split("\n")

incomplete_lines = []
error_scores = []

for i_line, line in enumerate(lines):
	line_ = line
	while True:
		line = line_
		line_= line_.replace("()", "")
		line_= line_.replace("[]", "")
		line_= line_.replace("{}", "")
		line_= line_.replace("<>", "")
		if len(line_) == len(line):	break

	n_open = sum([1 for c in line if c in chars_open  ])
	n_close= sum([1 for c in line if c in chars_close ])
	if n_open == 0 or n_close == 0: 
		incomplete_lines.append(line)
		continue

	for c in chars_open: line = line.replace(c, "")
	error_scores.append(error_score[line[0]])

print("Part 1 :", sum(error_scores))



closing_lines = [ [ open_to_close[char] for char in line[::-1] ] for line in incomplete_lines ]
autocomplete_scores = [ functools.reduce(lambda total, char : total*5 + autocomplete_score[char], line, 0) for line in closing_lines ]
print("Part 2 :", sorted(autocomplete_scores)[len(autocomplete_scores)//2])