

#Simple LED-Warrior14 scratch for send data
from __future__ import print_function
import sys
import time
import smbus #use smbus for i2c
from time import sleep

#return values
RET_ERROR	= -1
RET_NONO	= 0
RET_SUCCESS	= 1


#I2C device addresses
LW14_I2C_ADDRESS_1	= 0x23 #7Bit Address Regal 2 Right
LW14_I2C_ADDRESS_2	= 0x2F #7Bit Address Regal 1 Left
LW14_I2C_ADDRESS_3	= 0x27 #7Bit Address Front Ambience
LW14_I2C_ADDRESS_4	= 0x2B #7Bit Address Back Ambience

I2C_values = {}
I2C_values[1]=LW14_I2C_ADDRESS_1
I2C_values[2]=LW14_I2C_ADDRESS_2
I2C_values[3]=LW14_I2C_ADDRESS_3
I2C_values[4]=LW14_I2C_ADDRESS_4

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


print("in lwheadmodule line 131")
#Select I2C interface UNCOMMENT on RPI
i2c = smbus.SMBus(1)
print("in lwheadmodule line 134")

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
			#print("in WaitForReady, r is", r)
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


	



#create dictionary mapping box names to dali addresses
box_dict = {}
F=open('box_to_dali_map.txt')
for line in F:
	box_dict[line.rstrip().split(',')[0]]=int(line.rstrip().split(',')[1])
	
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

	