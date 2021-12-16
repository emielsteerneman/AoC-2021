hex_input = open("input.txt").read()

hex_chars = "0123456789ABCDEF"

bitstring = "".join([ "{0:b}".format(hex_chars.index(char)).rjust(4, "0") for char in hex_input ])

print(bitstring)
print("110100101111111000101000")

def get(bs, n) : return bs[:n], bs[n:]

def get_literal(bitstring):
	literal_string = ""
	while True:
		bits, bitstring = get(bitstring, 5)
		end, bits = get(bits, 1)
		literal_string += bits
		if end == "0": break
	print(literal_string, int(literal_string, 2))
	return int(literal_string, 2), bitstring


packet_version, bitstring = get(bitstring, 3)
packet_type_id, bitstring = get(bitstring, 3)
print(packet_version, packet_type_id, bitstring)

literal, bitstring = get_literal(bitstring)

