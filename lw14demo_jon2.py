#!/usr/bin/python

#Simple LED-Warrior14 scratch for send data

import sys
import time
import smbus #use smbus for i2c
from time import sleep

#I2C device addresses
LW14_I2C_ADDRESS_1	= 0x23 #7Bit default address from LW14
LW14_I2C_ADDRESS_2	= 0x00 #7Bit 
LW14_I2C_ADDRESS_3	= 0x00 #7Bit 
LW14_I2C_ADDRESS_4	= 0x00 #7Bit 

#Register of LED-Warrior14
LW14_REG_STATUS			= 0x00 # Read only
LW14_REG_COMMAND		= 0x01 # Write/Read
LW14_REG_CONFIG			= 0x02 # Write only
LW14_REG_SIGNATURE 		= 0xF0 # Read only
LW14_REG_ADDRESS 		= 0xFE # Write only

#Answers of 'status' register
LW14_STATE_BUS_FAULT	= 0x80
LW14_STATE_BUSY 		= 0x40
LW14_STATE_OVERRUN 		= 0x20
LW14_STATE_FRAMEERROR 	= 0x10
LW14_STATE_VALID 		= 0x08
LW14_STATE_TIMEFRAME 	= 0x04
LW14_STATE_2BYTE 		= 0x02
LW14_STATE_1BYTE 		= 0x01
LW14_STATE_NONE 		= 0x00

#Value for 'config' register 
#1 = lowest, 5 = highest, other will be clipped
LW14_CONFIG_PRIO_1		= 0x01
LW14_CONFIG_PRIO_2		= 0x02 # Default value
LW14_CONFIG_PRIO_3		= 0x03
LW14_CONFIG_PRIO_4		= 0x04
LW14_CONFIG_PRIO_5		= 0x05

#Special bits for DALI address
LW14_MODE_DACP 	= 0
LW14_MODE_CMD  	= 1
LW14_ADR_SINGLE = 0
LW14_ADR_GROUP  = 1

LW14_MAX_SINGLE = 64
LW14_MAX_GROUP  = 16
LW14_MAX_DACP   = 254


#Select I2C interface
i2c = smbus.SMBus(1)

class lw14:
	def __init__(self):
		self.i2c_bus = 0	#I2C address for the specific LW14
		self.dali_adr = 0	#DALI address 

	#send method from SMBus API from linux / python
	def _i2c_send(self, data):

		#try to send data
		try:
			return i2c.write_i2c_block_data(self.i2c_bus, LW14_REG_COMMAND, data)
		except IOError as e:
			print ("I/O error({0}): {1}".format(e.errno, e.strerror))     
		
		return 0

	#generate the dali address in the following pattern:   Y AAA AAA S
	#Y -> set 1 for groups, 0 for single device
	#AAA AAA -> the adress. for single 0...63, for group 0...15
	#S -> set 1 for COMMANDS, 0 for DACP
	def SetDaliAddress(self, adr, y, s):
		self.dali_adr = (y | (adr << 1) | s)
		return self.dali_adr

	#set the i2c address for the class
	def SetI2cBus(self, i2c):
		self.i2c_bus = i2c

	def SendData(self, value):
		#array to send
		data = [self.dali_adr, value]
		return self._i2c_send(data)


dali_tab = [(4,200),(29,200),(26,200),(30,180),(7,190)]



#run the programm
if __name__ == "__main__":

	#if some arguments given, use this as data. 
	#len = 3, because filename is [0], dali-address is [1], dali-data is[2]
	print("sys.argv",sys.argv)
	if len(sys.argv) == 3:
		dali_device = int(sys.argv[1])
		dali_value = int(sys.argv[2])

		#print out the args
		for eachArg in sys.argv:
			print eachArg

	#If no arguments ar set or to much send this to dali
	else:
		print("in else")
		dali_device = 19			#0...63 for single, or 0...16 for group
		dali_value = 254			#DACP values (dimming output) 0...254 allowed
	print("Dali device, value is",dali_device,dali_value)
	print("dali_tab is", dali_tab)
	DaliBus_Bar1 = lw14()
	for i,j in dali_tab:
		dali_device = i
		dali_value = j
		print("in loop, dali_device, dali_value are  ",dali_device,dali_value)
		#DaliBus_Bar1 = lw14()														#Create a new lw14 class
		DaliBus_Bar1.SetI2cBus(LW14_I2C_ADDRESS_1)									#Set I2C-Address to the class
		DaliBus_Bar1.SetDaliAddress(dali_device, LW14_ADR_SINGLE, LW14_MODE_DACP)	#Set the dali address for send data, in this case single device and DACP bit
		DaliBus_Bar1.SendData(dali_value)											#Send data into the dali bus
		print("sleeping")
		sleep(1)
