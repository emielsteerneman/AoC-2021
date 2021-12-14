string, mappings_input = open("input.txt").read().split("\n\n")

mappings_single = {} # HO -> F : mappings_single[HO] = F
mappings_pairs  = {} # HO -> F : mappings_pairs [HO] = [ HF, FO ]

for mapping in mappings_input.split("\n"):
	k, v = mapping.split(" -> ")
	mappings_single[k] = v
	mappings_pairs[k] = [ k[0]+v, v+k[1] ]

# quantities_pairs[ HO ] = 0
quantities_pairs  = { k : 0 for k in mappings_pairs }
# quantities_single[ F ] = 0
quantities_single = { v : 0 for _, v in mappings_single.items() }

# Add letter pairs in initial string to quantities_pairs
for a,b in zip(string, string[1:]):	quantities_pairs[ a+b ] += 1
# Add letters in initial string to quantities_single
for char in string: quantities_single[char] += 1

for i in range(40):
	quantities_pairs_next = { k : 0 for k in quantities_pairs }
	for key in quantities_pairs:
		m1, m2 = mappings_pairs[key] 										# [HO] = [ HF, FO ]
		quantities_pairs_next[m1] += quantities_pairs[key]					# HF += HO
		quantities_pairs_next[m2] += quantities_pairs[key]					# HF += HO
		quantities_single[ mappings_single[key] ] += quantities_pairs[key]  # F  += HO

	quantities_pairs = quantities_pairs_next

	if i == 9 or i == 39:
		quantities = sorted([ quantities_single[v] for v in quantities_single ])
		print("Answer :", quantities[-1] - quantities[0])