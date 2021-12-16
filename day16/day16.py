def to_bitstring(string):
	hex_chars = "0123456789ABCDEF"	
	return "".join([ "{0:b}".format(hex_chars.index(char)).rjust(4, "0") for char in string ])

def get(bs, n) : return bs[:n], bs[n:]

def get_int(bs, n) : return int(bs[:n], 2), bs[n:]

def get_literal(bitstring):
	literal_string = ""
	while True:
		bits, bitstring = get(bitstring, 5)
		end, bits = get(bits, 1)
		literal_string += bits
		if end == "0": break
	return int(literal_string, 2), bitstring

version_total = 0

def parse_packet(bitstring, indent=0):
	global version_total

	packet_version, bitstring = get_int(bitstring, 3)
	packet_type_id, bitstring = get_int(bitstring, 3)	
	version_total += packet_version

	# Literal
	if packet_type_id == 4: return get_literal(bitstring)
	
	# Operator
	length_type_id, bitstring = get_int(bitstring, 1)

	literals = []

	if length_type_id == 0:
		packet_length, bitstring = get_int(bitstring, 15)
		subpacket, bitstring = get(bitstring, packet_length)
		while len(subpacket):
			literal, subpacket = parse_packet(subpacket, indent+1)
			literals.append(literal)
	else:
		n_subpackets, bitstring = get_int(bitstring, 11)
		for i in range(n_subpackets):
			literal, bitstring = parse_packet(bitstring, indent+1)
			literals.append(literal)

	if packet_type_id == 0:
		return sum(literals), bitstring 

	if packet_type_id == 1:
		final = 1
		for v in literals: final *= v
		return final, bitstring

	if packet_type_id == 2:
		return min(literals), bitstring

	if packet_type_id == 3:
		return max(literals), bitstring

	if packet_type_id == 5:
		final = 1 if literals[1] < literals[0] else 0
		return final, bitstring

	if packet_type_id == 6:
		final = 1 if literals[0] < literals[1] else 0
		return final, bitstring

	if packet_type_id == 7:
		final = 1 if literals[0] == literals[1] else 0
		return final, bitstring

bitstring = to_bitstring( open("input.txt").read() )
output, _ = parse_packet(bitstring)

print("Part 1:", version_total)
print("Part 2:", output)