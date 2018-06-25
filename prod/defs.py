''' FILE WITH DEFINES / CONST FOR THE WHOLE PROJECT RECEIVED 20180620'''

#return values
RET_NO_DALI   = -2
RET_ERROR     = -1
RET_NONE      = 0
RET_SUCCESS   = 1


RET_BUSFAULT  = -10
RET_ZERO      = -20


#I2C device addresses
LW14_I2C_ADDRESS_1	= 0x23 #7Bit Address Regal 2 Right
LW14_I2C_ADDRESS_2	= 0x2F #7Bit Address Regal 1 Left
LW14_I2C_ADDRESS_3	= 0x27 #7Bit Address Front Ambience
LW14_I2C_ADDRESS_4	= 0x2B #7Bit Address Back Ambience






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
DALI_ENABLE_DACP_SEQUENCE   = 0x09
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