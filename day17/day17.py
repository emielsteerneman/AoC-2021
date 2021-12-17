import math
import numpy as np
import cv2

# tx_min, tx_max, ty_min, ty_max = 20, 30, -10, -5
tx_min, tx_max, ty_min, ty_max = 277, 318, -92, -53

def shoot(vx, vy):
	x, y = 0, 0
	while True:
		x, y = x + vx, y + vy
		vx, vy = max(0, vx - 1), vy - 1
	
		if tx_min <= x <= tx_max and ty_min <= y <= ty_max: return True
		if tx_max < x or y < ty_min: return False
		
	return inside, x, y, max_x, max_y

def finite_sum(x):
	return x * (x+1) // 2

print("Part 1:", finite_sum(ty_min) )
x_vel_min = 0

""" Some optimization that I really like, but only gives a 20% performance boost

def solve_finite_sum(y):
	# x * (x+1) / 2 = y
	# x**2 + x  + 2y = 0
	return solve_quadratic(1, 1, -y*2)

def solve_quadratic(a, b, c):
	d = b**2 - 4 * a * c
	s1 = (-b - math.sqrt(d)) / (2*a)
	s2 = (-b + math.sqrt(d)) / (2*a)
	return max(s1, s2)

x_vel_min = math.ceil(solve_finite_sum(tx_min))

"""

total = 0
for vx in range(x_vel_min, tx_max + 1):
	for vy in range(ty_min, -ty_min):
		if shoot(vx, vy): total += 1
print("Part 2:", total)