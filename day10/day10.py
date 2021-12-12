import functools
import re

open_to_close = { "(":")", "[":"]", "{":"}", "<":">" }
error_score = {")":3, "]":57, "}":1197, ">":25137}
autocomplete_score = {")":1, "]":2, "}":3, ">":4}

lines = open("input.txt").read().strip().split("\n")

incomplete_lines = []
error_scores = []

for line in lines:
	while True:
		length = len(line)
		line = re.sub(r"\(\)|\[\]|{}|<>", "", line)		
		if len(line) == length: break

	line_closed = re.sub(r"\(|\[|{|<", "", line)		
	if len(line_closed):
		error_scores.append(error_score[line_closed[0]])
	else:
		incomplete_lines.append(line)
	
print("Part 1 :", sum(error_scores))

closing_lines = [ [ open_to_close[char] for char in line[::-1] ] for line in incomplete_lines ]
autocomplete_scores = [ functools.reduce(lambda total, char : total*5 + autocomplete_score[char], line, 0) for line in closing_lines ]
print("Part 2 :", sorted(autocomplete_scores)[len(autocomplete_scores)//2])