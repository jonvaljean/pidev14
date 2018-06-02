#!/usr/bin/python

#Simple LED-Warrior14 scratch for send data
from __future__ import print_function
import sys
import time
import smbus #use smbus for i2c
from time import sleep
from bottle import route, run, template, get, post, request
import subprocess

#return values
RET_ERROR	= -1
RET_NONO	= 0
RET_SUCCESS	= 1


#I2C device addresses
LW14_I2C_ADDRESS_1	= 0x23 #7Bit default address from LW14
LW14_I2C_ADDRESS_2	= 0x2f #7Bit 
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
LW14_MODE_DACP 	= 0x00	#0
LW14_MODE_CMD  	= 0x01  #1
LW14_ADR_SINGLE = 0x00	#0
LW14_ADR_GROUP  = 0x80 	#1

LW14_MAX_SINGLE = 64
LW14_MAX_GROUP  = 16
LW14_MAX_DACP   = 254

LW14_BROADCAST  = 0x3F 


#DALI Commands
DALI_OFF					= 0x00
DALI_UP						= 0x01
DALI_DOWN					= 0x02
DALI_STEP_UP				= 0x03
DALI_STEP_DOWN				= 0x04
DALI_MAX					= 0x05
DALI_MIN					= 0x06
DALI_STEP_DOWN_OFF			= 0x07
DALI_ON_STEP_UP				= 0x08
DALI_SCENE					= 0x10	#0x10 - 0x1F
DALI_SCENE_MASK				= 0x1F
DALI_RESET					= 0x20
DALI_DTR_ACTUAL_LEVEL		= 0x21
DALI_DTR_MAX_LEVEL			= 0x2A
DALI_DTR_MIN_LEVEL			= 0x2B
DALI_DTR_SYS_FAIL_LEVEL		= 0x2C
DALI_DTR_POWER_ON_LEVEL		= 0x2D
DALI_DTR_FADE_TIME			= 0x2E
DALI_DTR_FADE_RATE			= 0x2F
DALI_ADD_SCENE				= 0x40	#0x40 - 0x4F
DALI_REMOVE_SCENE			= 0x50	#0x50 - 0x5F
DALI_ADD_GROUP				= 0x60	#0x60 - 0x6F
DALI_REMOVE_GROUP			= 0x70	#0x70 - 0x7F
DALI_DTR_AS_SHORT_ADDRESS 	= 0x80
DALI_DTR_0					= 0xA3

DALI_QUERY_STATUS						= 0x90
DALI_QUERY_CONTROL_GEAR					= 0x91	#Antwort : Ja oder Nein
DALI_QUERY_LAMP_FAILURE					= 0x92	#Antwort : Ja oder Nein
DALI_QUERY_LAMP_POWER_ON				= 0x93	#Antwort : Ja oder Nein
DALI_QUERY_LIMIT_ERROR					= 0x94	#Antwort : Ja oder Nein
DALI_QUERY_RESET_STATE					= 0x95	#Antwort : Ja oder Nein
DALI_QUERY_MISSING_SHORT_ADDRESS		= 0x96	#Antwort : Ja oder Nein
DALI_QUERY_VERSION_NUMBER				= 0x97	#Antwort : Muss 1 Sein
DALI_QUERY_CONTENT_DTR					= 0x98	#Antwort : Inhalt des DTR (8 Bit)
DALI_QUERY_DEVICE_TYPE					= 0x99	#Antwort : Wert zwischen 0..255
DALI_QUERY_PHYSICAL_MIN_LEVEL			= 0x9A	#Antwort : 8 Bit Wert
DALI_QUERY_POWER_FAILURE				= 0x9B	#Antwort : Ja, wenn nach Einschalten kein RESET, DAPC, OFF, RECALL MAX LEVEL, RECAL MIN LEVEL, STEP DOWN AND OFF, ON AND STEP UP, TO TO SCENE
DALI_QUERY_CONTENT_DTR1					= 0x9C	#Antwort : Inhalt des DTR1 (8 Bit)
DALI_QUERY_CONTENT_DTR2					= 0x9D	#Antwort : Inhalt des DTR2 (8 Bit)					
DALI_QUERY_ACTUAL_LEVEL					= 0xA0	#Antwort : Aktuelle Ausgabewert (0...254)
DALI_QUERY_MAX_LEVEL					= 0xA1	#Antwort : Eingestellter MAX Wert
DALI_QUERY_MIN_LEVEL					= 0xA2	#Antwort : Eingestellter MIN Wert
DALI_QUERY_POWER_ON_LEVEL				= 0xA3	#Antwort : Eingestellter POWER ON Wert
DALI_QUERY_SYSTEM_FAILURE_LEVEL			= 0xA4	#Antwort : Eingestellter SYSTEM FAILURE Wert
DALI_QUERY_FADE_TIME_RATE				= 0xA5	#Antwort : Eingestellter FADE TIME(X) und FADE RATE(Y) werte (8 Bit: XXXX YYYYY)	
DALI_QUERY_SCENE_LEVEL					= 0xB0	#0xB0 - 0xBF Antwort : Lampenleistung der Scene (8 Bit)



#values for Fadetime and fade rate. Time is in seconds, Rate is in steps/second
#fadetime = [0,0.7,1.0,1.4,2.0,2.8,4.0,5.7,8.0,11.3,16.0,22.6,32.0,45.3,64.0,90.5] #value to dali -> 0 ... 15
#faderate = [0,358,253,179,127,89.4,63.3,44.7,31.6,22.4,15.8,11.2,7.9,5.6,4.0,2.8] #value to dali -> 0 ... 15  -> 0 is impossible!

#DALI default values
DALI_DEFAULT_MAX = 254
DALI_DEFAULT_MIN = 1
DALI_DEFAULT_SYSTEM_FAIL = 254
DALI_DEFAULT_POWER_ON = 254
DALI_DEFAULT_FADE_RATE = 7
DALI_DEFAULT_FADE_TIME = 0



#Select I2C interface UNCOMMENT on RPI
i2c = smbus.SMBus(1)

class lw14:
	def __init__(self):
		self.i2c_bus = 0	#I2C address for the specific LW14
		self.dali_adr = 0	#DALI address 
		self.dali_mode = LW14_MODE_DACP

	#send method from SMBus API from linux / python
	def _i2c_write(self, data):
  	        
	    #try to send data
	    try:
	        return i2c.write_i2c_block_data(self.i2c_bus, LW14_REG_COMMAND, data)
	    except IOError as e:
	        print ("I/O error({0}): {1}".format(e.errno, e.strerror))
	        return RET_ERROR

	def _i2c_read(self, reg):

		try:
			return i2c.read_i2c_block_data(self.i2c_bus, reg)
		except IOError as e:
			print ("I/O error({0}): {1}".format(e.errno, e.strerror))
			return RET_ERROR

	#generate the dali address in the following pattern:   Y AAA AAA S
	#Y -> set 1 for groups, 0 for single device
	#AAA AAA -> the adress. for single 0...63, for group 0...15, for broadcast (all devices) Y=1 and AAA AAA = 63
	#S -> set 1 for COMMANDS, 0 for DACP
	def SetDaliAddress(self, adr, y, s):
		self.dali_adr = (y | (adr << 1) | s)
		return self.dali_adr

	def SetMode(self, s):
		self.dali_mode = s
		return self.dali_mode

	#set the i2c address for the class
	def SetI2cBus(self, i2c):
		self.i2c_bus = i2c

	#Check the status register
	def WaitForReady(self):
		while(1):
			
			r = self._i2c_read(LW14_REG_STATUS) #returns an array

			#debug output
			#print ("Status: {0}".format(r[0]))
		
			if (r[0] & LW14_STATE_BUS_FAULT) == LW14_STATE_BUS_FAULT:
				return RET_ERROR

			elif (r[0] & LW14_STATE_BUSY) != LW14_STATE_BUSY:
				#print ("Bus ready")
				return RET_SUCCESS

			elif r[0] == RET_ERROR:
				return RET_ERROR

	#Wait until possible data will available
	def WaitForValidReply(self):
		while(1):
			#sleep(0.005)
			r = self._i2c_read(LW14_REG_STATUS) #returns an array

			if (r[0] & LW14_STATE_BUS_FAULT) == LW14_STATE_BUS_FAULT:
				return RET_ERROR

			elif (r[0] & (LW14_STATE_VALID | LW14_STATE_1BYTE) ) == (LW14_STATE_VALID | LW14_STATE_1BYTE):
				#self._i2c_read(LW14_REG_COMMAND) #returns an array
				return RET_SUCCESS

			elif r[0] == 0x00:
				return RET_NONE


	#store commands must be send twice
	def SendStore(self, data):
		ret = self._i2c_write(data)
		if ret != RET_ERROR:
			self.WaitForReady()
			ret = self._i2c_write(data)
			return RET_SUCCESS
		else:
			return RET_ERROR

	#Send data to the device
	def SendData(self, value):
		#array to send
		data = [self.dali_adr, value]
		return self._i2c_write(data)

	#set a value into DTR of all devices on DALI bus 	
	def SetDTR(self, value):
		data = [DALI_DTR_0, value] 
		return self._i2c_write(data)			

	### Store commands ###
	def StoreActualToDTR(self):
		data = [self.dali_adr, DALI_DTR_ACTUAL_LEVEL]
		return self._i2c_write(data)	

	def StoreMin(self):
		data = [self.dali_adr, DALI_DTR_MIN_LEVEL]
		return self.SendStore(data)	

	def StoreMax(self):
		data = [self.dali_adr, DALI_DTR_MAX_LEVEL]
		return self.SendStore(data)	

	def StoreSysFail(self):
		data = [self.dali_adr, DALI_DTR_SYS_FAIL_LEVEL]
		return self.SendStore(data)	

	def StorePowerOn(self):
		data = [self.dali_adr, DALI_DTR_POWER_ON_LEVEL]
		return self.SendStore(data)	

	#Valid values from 0...15
	def StoreFadeRate(self):
		data = [self.dali_adr, DALI_DTR_FADE_RATE]
		return self.SendStore(data)	

	#Valid values from 0...15
	# 0-> no fading
	def StoreFadeTime(self):
		data = [self.dali_adr, DALI_DTR_FADE_TIME]
		return self.SendStore(data)	
		
	#store the DTR value as scene value for device and scene
	def StoreScene(self, value):
		data = [self.dali_adr, 0x40 | (value & 0x0F)] 
		return self.SendStore(data)			

	#remove data from scene (without DTR values)
	def RemoveScene(self, value):
		adr = self.dali_adr | LW14_MODE_CMD
		data = [adr, 0x50 | (value & 0x0F)] 
		return self.SendStore(data)			

	def StoreGroup(self, value):
		adr = self.dali_adr | LW14_MODE_CMD
		data = [adr, 0x60 | (value & 0x0F)]
		return self.SendStore(data)	

	def RemoveGroup(self, value):
		adr = self.dali_adr | LW14_MODE_CMD
		data = [adr, 0x70 | (value & 0x0F)]
		return self.SendStore(data)	

	#Read data from DALI device
	def ReadQuery(self, value):
		data = [self.dali_adr, value]
		self._i2c_write(data)
		if self.WaitForValidReply() == RET_SUCCESS:
			read = self._i2c_read(LW14_REG_COMMAND)
		else:
			print ("something goes wrong or no device on this address")
		
		#Clear command register
		self._i2c_read(LW14_REG_COMMAND)

		return read[0]
	
	#Get values from querys
	def QueryDTR(self):
		return self.ReadQuery(DALI_QUERY_CONTENT_DTR)

	def QueryMin(self):
		return self.ReadQuery(DALI_QUERY_MIN_LEVEL)

	def QueryMax(self):
		return self.ReadQuery(DALI_QUERY_MAX_LEVEL)

	def QuerySysFail(self):
		return self.ReadQuery(DALI_QUERY_SYSTEM_FAILURE_LEVEL)

	def QueryPowerOn(self):
		return self.ReadQuery(DALI_QUERY_POWER_ON_LEVEL)

	def QueryFadeRate(self):
		r = self.ReadQuery(DALI_QUERY_FADE_TIME_RATE)		
		return (r & 0x0F)

	def QueryFadeTime(self):
		r = self.ReadQuery(DALI_QUERY_FADE_TIME_RATE)	
		return (r & 0xF0) >> 4

bar_group = []
COLUMN_LABEL = "LEFT"
#COLUMN_LABEL = "RIGHT"

#colums for right side
if COLUMN_LABEL == "RIGHT":
	bar_group.append((28,8,4,0,14,27))
	bar_group.append((16,37,17,29,22,10))
	bar_group.append((1,13,15,26,39,19))
	bar_group.append((5,32,20,42,9,25,40))
	bar_group.append((31,21,11,6,30,36))
	bar_group.append((34,35,12,38,41,33,18))
	bar_group.append((43,2,23,3,7,24))  
	print("bar_group is ",bar_group)
	print("bar_group[3] is ", bar_group[3])

if COLUMN_LABEL == "LEFT":
#colums for left side
	bar_group.append((4,0,25,19,9,16))
	bar_group.append((31,23,11,18,21,33))
	bar_group.append((8,18,2,7,1,24,15))
	bar_group.append((5,10,6,12,34,13))
	bar_group.append((28,35,3,26,14,22))
	bar_group.append((32,20,30,29,36,27))
	print("bar_group is ",bar_group)
	print("bar_group[3] is ", bar_group[3])


def doit_single(DaliBus_Bar1,device, value):
	DaliBus_Bar1.SetI2cBus(LW14_I2C_ADDRESS_2)									#Set I2C-Address to the class
	dali_device = device
	dali_value = value
	DaliBus_Bar1.SetDaliAddress(dali_device, LW14_ADR_SINGLE, LW14_MODE_DACP)	    #Set the dali address for send data, in this case single device and DACP bit
	DaliBus_Bar1.SendData(dali_value)												#Send data into the dali bus
	DaliBus_Bar1.WaitForReady() 													#Wait until DALI is ready. DON'T FORGET IT!!!!!
	return


def doit_group(DaliBus_Bar1,col_id,value):
	DaliBus_Bar1.SetI2cBus(LW14_I2C_ADDRESS_2)									#Set I2C-Address to the class
	dali_device = col_id
	dali_value = value
	DaliBus_Bar1.SetDaliAddress(dali_device, LW14_ADR_GROUP, LW14_MODE_DACP)				#Must be in CMD mode !
	DaliBus_Bar1.SendData(dali_value)													#Send data to group
	DaliBus_Bar1.WaitForReady() 													#Wait until DALI is ready. DON'T FORGET IT!!!!!
	return
	
	
	#run the programm
if __name__ == "__main__":

	@route('/hello/<name>')
	def index(name):
		return template('<b>Hello {{name}}</b>!',name=name)
		print("in bottlepy route  ")


	@route('/lw14ask')
	def lw14ask():
		return'''
			<form action="/lw14_group" method="POST">
				<br>
				Group <input type="text" name="group_id"/>  : Intensity value <input type="text" name="group_intensity"/> <input value="Group" type="submit" />
			</form>
			<form action="/lw14_single" method="POST">
				<br>
				Single <input type="text" name="single_id"/>  : Intensity value <input type="text" name="single_intensity"/> <input value="Single" type="submit" />
			</form>
		'''
		
	@route('/lw14_group', method='POST')
	def lw14_group():
		DaliBus_Bar1 = lw14()														#Create a new lw14 class
		print("in handler, DaliBus_Bar1 is  ", DaliBus_Bar1)
		g_id = int(request.forms.get('group_id'))
		g_intensity = int(request.forms.get('group_intensity'))
		print("in lw14_group handler, g_id and g_intensity are ",g_id,g_intensity)
		doit_group(DaliBus_Bar1,g_id,g_intensity)
		
	@route('/lw14_single', method='POST')
	def lw14_single():
		DaliBus_Bar1 = lw14()
		s_id = int(request.forms.get('single_id'))
		s_intensity = int(request.forms.get('single_intensity'))
		print("in lw14_single handler, s_id and s_intensity are ",s_id,s_intensity)
		doit_single(DaliBus_Bar1,s_id,s_intensity)
		
	@route('/spawn')
	def spawn():
		return '<pre>%s</pre>'%subprocess.Popen(["./lwturnboxon.py","c5"],stdout=subprocess.PIPE).communicate()[0]
		#subprocess.run('sudo','python','./lwturnboxon','c5')
		#return template('<b>Spawned  {{name}}</b>!',name='lwturnboxon')
		
	run(host='0.0.0.0', port=80, debug=True)
	print("in bottlepy after run   ")
		
		
		
"""	
	#if some arguments given, use this as data. 
	#len = 3, because filename is [0], dali-address is [1], dali-data is[2]
	if len(sys.argv) == 3:
		dali_device = int(sys.argv[1])
		dali_value = int(sys.argv[2])

		#print out the args
		#for eachArg in sys.argv:
		#	print eachArg

	#If no arguments ar set or to much send this to dali
	else:
		dali_device = 1			#0...63 for single, or 0...16 for group
		dali_value = 200			#DACP values (dimming output) 0...254 allowed
"""
  
  #Cycle through bar_group to set each box to its group
"""
  
	col_id = 0
	for column in bar_group:
		col_id +=1
		print("col_id is",col_id)
		for dali_device in column:
			dali_value = col_id
			print('dali_device, col_id:  ',dali_device, col_id)
			#DaliBus_Bar1.SetDaliAddress(dali_device, LW14_ADR_SINGLE, LW14_MODE_CMD)	#Must be in CMD mode !
			#DaliBus_Bar1.StoreGroup(dali_value)													#Set device into group
  
  #Test all columns turning on and off
  
	col_id = 0
	for column in bar_group:
		col_id +=1
		print("col_id is",col_id)
		dali_device = col_id
		dali_value = 255
		DaliBus_Bar1.SetDaliAddress(dali_device, LW14_ADR_GROUP, LW14_MODE_DACP)				#Must be in CMD mode !
		DaliBus_Bar1.SendData(dali_value)													#Send data to group
		print("turned on ....")
		sleep(0,5)
		dali_value = 0
		DaliBus_Bar1.SendData(dali_value)	
		print("turned off ...")
		sleep(1)
  
	#Send Data test
	#DaliBus_Bar1.SetDaliAddress(dali_device, LW14_ADR_SINGLE, LW14_MODE_DACP)	    #Set the dali address for send data, in this case single device and DACP bit
	#DaliBus_Bar1.SetDaliAddress(LW14_BROADCAST, LW14_ADR_GROUP, LW14_MODE_DACP)	#Set the dali as broadcast
	#DaliBus_Bar1.SendData(dali_value)												#Send data into the dali bus
	#DaliBus_Bar1.WaitForReady() 													#Wait until DALI is ready. DON'T FORGET IT!!!!!




	#Store tests
	#DaliBus_Bar1.SetDaliAddress(dali_device, LW14_ADR_SINGLE, LW14_MODE_CMD)	#Must be in CMD mode !
	
	#DaliBus_Bar1.SetDTR(dali_value)													#Set a value into the DTR
	#DaliBus_Bar1.WaitForReady() 												#Wait until DALI is ready. DON'T FORGET IT!!!!!

	#DaliBus_Bar1.StoreScene(dali_value)			#Store DTR into scene 1 for the selected device (dali_device)
	#DaliBus_Bar1.StoreMax()						#Store DTR as default MAX
	



	#Group tests
	#DaliBus_Bar1.SetDaliAddress(dali_device, LW14_ADR_SINGLE, LW14_MODE_CMD)	#Must be in CMD mode !
	#DaliBus_Bar1.StoreGroup(dali_value)													#Set device into group
	#DaliBus_Bar1.RemoveGroup(dali_value)												#Remove from group

	#DaliBus_Bar1.SetDaliAddress(dali_device, LW14_ADR_GROUP, LW14_MODE_DACP)				#Must be in CMD mode !
	#DaliBus_Bar1.SendData(dali_value)													#Send data to group


	#Query/Read tests
	#Read data from device. Use this only for devices. Groups or broadcast is not allowed!
	#DaliBus_Bar1.SetDaliAddress(dali_device, LW14_ADR_SINGLE, LW14_MODE_CMD)
	#data = DaliBus_Bar1.QueryMax()
	#print ("Read: {0}".format(data))
	
	
	"""
