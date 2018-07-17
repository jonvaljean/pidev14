'''Read Dali assignments from files to create internal map in form of dicts'''
import defs

I2C_values = {}
I2C_values[1]=defs.LW14_I2C_ADDRESS_1
I2C_values[2]=defs.LW14_I2C_ADDRESS_2
I2C_values[3]=defs.LW14_I2C_ADDRESS_3
I2C_values[4]=defs.LW14_I2C_ADDRESS_4

#create dictionary mapping box names to dali addresses
box_dict = {}
F=open('box_to_dali_map.txt')
counter=1
for line in F:
	box_dict[line.rstrip().split(',')[0]]=int(line.rstrip().split(',')[1])
	counter += 1
	print("counter is ", counter)
print("length of box_dict is   ",len(box_dict))
#create dictionary mapping column to appropriate dali network
net_dict = {}
F=open('col_to_dali_net_map.txt')
for line in F:
	net_dict[line.rstrip().split(',')[0]]=int(line.rstrip().split(',')[1])

#create dictionary mapping column to group number
grp_dict = {}
F=open('col_to_dali_net_map.txt')
for line in F:
	grp_dict[line.rstrip().split(',')[0]]=int(line.rstrip().split(',')[2])	
