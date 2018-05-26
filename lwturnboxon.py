#!/usr/bin/python

from __future__ import print_function
import sys
import time
import smbus #use smbus for i2c
from time import sleep
from lwheadmodule import *
	
	#modify this model according to requirements of setting
NR_ARGS = 1
	
	#run the programm
if __name__ == "__main__":

	#if some arguments given, use this as data. 
	#len = 3, because filename is [0], dali-address is [1], dali-data is[2]
	if len(sys.argv) == NR_ARGS+1:
		parm_1 = sys.argv[1]
		#parm_2 = int(sys.argv[2])
		#parm_3 = int(sys.argv[3])

		#print out the args
		#for eachArg in sys.argv:
		#	print eachArg

	#If no arguments ar set or to much send this to dali
	else:
		print("Wrong number of parameters")
		sys.exit(0)
		
	DaliBus_Bar1 = lw14()														#Create a new lw14 class
	dali_bus = I2C_values[net_dict[parm_1[0]]]
	DaliBus_Bar1.SetI2cBus(dali_bus)									#Set I2C-Address to the class
	dali_device = box_dict[parm_1]
	
	
		#choose between broadcast and single device. 255 is gotten from map table if x or y is chosen
	if dali_device == 255:
		dalibus.SetDaliAddress(LW14_BROADCAST, LW14_ADR_GROUP, LW14_MODE_CMD)	
	else:
		dalibus.SetDaliAddress(dali_device, LW14_ADR_SINGLE, LW14_MODE_CMD)
	
	dali_value = DALI_MAX

	#Send Data test
	#DaliBus_Bar1.SetDaliAddress(dali_device, LW14_ADR_SINGLE, LW14_MODE_CMD)	#Must be in CMD mode !

	#DaliBus_Bar1.SetDaliAddress(dali_device, LW14_ADR_SINGLE, LW14_MODE_DACP)	    #Set the dali address for send data, in this case single device and DACP bit
	#DaliBus_Bar1.SetDaliAddress(LW14_BROADCAST, LW14_ADR_GROUP, LW14_MODE_DACP)	#Set the dali as broadcast
	DaliBus_Bar1.SendData(dali_value)												#Send data into the dali bus
	DaliBus_Bar1.WaitForReady() 													#Wait until DALI is ready. DON'T FORGET IT!!!!!




	
