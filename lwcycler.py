#!/usr/bin/python

#Simple LED-Warrior14 scratch for send data
from __future__ import print_function
import sys
import time
import smbus #use smbus for i2c
from time import sleep
from lwheadmodule import *


	#modify this model according to requirements of setting
NR_ARGS = 4



	
	#run the programm
if __name__ == "__main__":

	DaliBus_Bar1 = lw14()
	
	#if some arguments given, use this as data. 
	#parm is cycle file name
	
	if len(sys.argv) == NR_ARGS+1:
		filename	= sys.argv[1]
		onval = sys.argv[2]
		offval = sys.argv[3]
		sleeptime = sys.argv[4]
		
		#If no arguments ar set or to much send this to dali
	else:
		print("Wrong number of parameters")
		sys.exit(0)
		
	F=open(filename)
	cmd_list = f.read().striplines()
	
	while True:
		for line in cmd_list:
			for cmd in line:
				dali_bus = I2C_values[net_dict[cmd[0]]]
				DaliBus_Bar1.SetI2cBus(dali_bus)
				dali_device = grp_dict[cmd[0]]
				if cmd[1] == "on": dali_value = onval
				if cmd[1] == "off": dali_value = offval
				DaliBus_Bar1.SetDaliAddress(dali_device, LW14_ADR_GROUP, LW14_MODE_DACP)	    #Set the dali address for send data, in this case single device and DACP bit
				DaliBus_Bar1.SendData(dali_value)												#Send data into the dali bus
				DaliBus_Bar1.WaitForReady() 													#Wait until DALI is ready. DON'T FORGET IT!!!!!
				sleep(sleeptime)



	
