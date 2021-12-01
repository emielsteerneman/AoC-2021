# 1
depths = open("input1.txt").read().strip().split("\n")
depths = [int(depth) for depth in depths]

depths_paired = list(zip(depths, depths[1:]))
depths_increased = [a<b for a, b in depths_paired]
print(f"Answer 1 : {sum(depths_increased)}")


# 2
depths = open("input1.txt").read().strip().split("\n")
depths = [int(depth) for depth in depths]

depths_window = list(zip(depths, depths[1:], depths[2:]))
depths_summed = [ sum([a,b,c]) for a,b,c in depths_window ]

depths_paired = list(zip(depths_summed, depths_summed[1:]))
depths_increased = [a<b for a, b in depths_paired]
print(f"Answer 2 : {sum(depths_increased)}")


# oneliners
print("Answer 1 :", sum([a<b for a, b in list(zip([int(depth) for depth in open("input1.txt").read().strip().split("\n")], [int(depth) for depth in open("input1.txt").read().strip().split("\n")][1:]))]))
print("Answer 2 :", sum([a<b for a, b in list(zip([ sum([a,b,c]) for a,b,c in list(zip([int(depth) for depth in open("input1.txt").read().strip().split("\n")], [int(depth) for depth in open("input1.txt").read().strip().split("\n")][1:], [int(depth) for depth in open("input1.txt").read().strip().split("\n")][2:])) ], [ sum([a,b,c]) for a,b,c in list(zip([int(depth) for depth in open("input1.txt").read().strip().split("\n")], [int(depth) for depth in open("input1.txt").read().strip().split("\n")][1:], [int(depth) for depth in open("input1.txt").read().strip().split("\n")][2:])) ][1:]))]))