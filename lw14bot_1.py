#!/usr/bin/python


from __future__ import print_function
import sys
import time
from time import sleep
from bottle import route, run, template, get, post, request, redirect
import subprocess


	
	
	#run the programm
if __name__ == "__main__":




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
			<form action="/cycle" method="POST">
				<br>
				Script <input type="text" name="script" /> : High <input type="text" name="high"/>  : Low <input type="text" name="low"/> <input value="Cycle" type="submit" />
			</form>
		'''
		
	@route('/lw14_group', method='POST')
	def lw14_group():
		#print("in handler, DaliBus_Bar1 is  ", DaliBus_Bar1)
		g_id = request.forms.get('group_id')
		g_intensity = request.forms.get('group_intensity')
		#print("in lw14_group handler, g_id and g_intensity are ",g_id,g_intensity)
		subprocess.Popen(["./lwturngrpto.py", g_id, g_intensity],stdout=subprocess.PIPE)[0]
		redirect("/lw14ask")
		
	@route('/lw14_single', method='POST')
	def lw14_single():
		s_id = request.forms.get('single_id')
		s_intensity = request.forms.get('single_intensity')
		#print("in lw14_single handler, s_id and s_intensity are ",s_id,s_intensity)
		subprocess.Popen(["./lwturnboxto.py", s_id, s_intensity],stdout=subprocess.PIPE)[0]
		redirect("/lw14ask")
		
	@route('/cycle', method='POST')
	def cycle():
		c_high = request.forms.get('high')
		c_low = request.forms.get('low')
		c_script = request.forms.get('script')
		print("input parms are  ",c_high, c_low, c_script)
		subprocess.Popen(["./lwcycler_test2.py", c_script,c_high, c_low],stdout=subprocess.PIPE).communicate()[0]
		redirect("/lw14ask")
		
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
