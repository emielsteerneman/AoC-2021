import re
import numpy as np

def parseLine(line):
	return np.array([ int(n) for n in re.split(r' +', line.strip()) ])

def parseBoard(lines):
	board = np.zeros((5, 5), dtype=np.uint8)
	for i, line in enumerate(lines):
		board[i, :] = parseLine(line)
	return board

def to_truth(matrix, numbers):
	def to_truth_(value):
		return value in numbers
	return np.vectorize(to_truth_)(matrix)

text = open("input.txt").read().split("\n")
numbers = list(map(int, text.pop(0).split(",")))
boards = [ parseBoard(text[i+1:i+6]) for i in range(0, len(text), 6) ]

print(f"Number of boards : {len(boards)}")

boards_completed = []

for idx in range(len(numbers)):

	for i_board, board in enumerate(boards):
		board_mask = to_truth(board, numbers[:idx])

		row_detected = np.any(np.all(board_mask, axis=1))
		col_detected = np.any(np.all(board_mask.T, axis=1))

		if row_detected or col_detected:
			board_ = np.copy(board)
			matrix_sum = int(np.sum(np.multiply(board_, ~board_mask)))
			answer = matrix_sum * numbers[idx-1]
			
			if len(boards_completed) == 0:
				print("First board : ", answer)

			if i_board not in boards_completed:
				boards_completed.append(i_board)
			
			if len(boards_completed) == len(boards):
				print("Last board : ", answer)
				exit()