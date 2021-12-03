numbers_ = open("input1.txt").read().strip().split("\n")
n_bits = len(numbers_[0])
numbers_ = [int(number, 2) for number in numbers_]



# Part 1
numbers = numbers_[:]
gamma = 0
for i in range(n_bits):
	total = sum([ 0 < (n & (1<<i)) for n in numbers])
	if len(numbers)/2 < total: gamma += 1 << i
epsilon = gamma^(2**n_bits-1)

print(gamma*epsilon)



# Part 2
numbers = numbers_[:]
for b in reversed(range(n_bits)):
	if len(numbers)==1: break
	total = sum([ 0 < (n & (1<<b)) for n in numbers])
	bit = 1 if len(numbers) / 2 <= total else 0
	numbers = [n for n in numbers if ( (n>>b)&1 ) == bit]
oxygen = numbers[0]

numbers = numbers_[:]
for b in reversed(range(n_bits)):
	if len(numbers)==1: break
	total = sum([ 0 < (n & (1<<b)) for n in numbers])
	bit = 0 if len(numbers) / 2 <= total else 1
	numbers = [n for n in numbers if ( (n>>b)&1 ) == bit]	
co2 = numbers[0]

print(co2 * oxygen)