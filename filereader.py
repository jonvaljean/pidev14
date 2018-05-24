box_dict = {}
F=open('box_to_dali_map.txt')
for line in F:
	box_dict[line.rstrip().split(',')[0]]=int(line.rstrip().split(',')[1])
print(box_dict)
print("test value of r3 is ", box_dict['r3'])