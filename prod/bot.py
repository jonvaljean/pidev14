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
		subprocess.Popen(["./grpto.py", g_id, g_intensity],stdout=subprocess.PIPE)
		redirect("/lw14ask")
		
	@route('/lw14_single', method='POST')
	def lw14_single():
		s_id = request.forms.get('single_id')
		s_intensity = request.forms.get('single_intensity')
		#print("in lw14_single handler, s_id and s_intensity are ",s_id,s_intensity)
		subprocess.Popen(["./boxto.py", s_id, s_intensity],stdout=subprocess.PIPE)
		redirect("/lw14ask")
		
	@route('/cycle', method='POST')
	def cycle():
		c_high = request.forms.get('high')
		c_low = request.forms.get('low')
		c_script = request.forms.get('script')
		print("input parms are  ",c_high, c_low, c_script)
		subprocess.Popen(["./cycler2.py", c_script,c_high, c_low, 2],stdout=subprocess.PIPE)
		redirect("/lw14ask")
		
	@route('/spawn')
	def spawn():
		return '<pre>%s</pre>'%subprocess.Popen(["./lwturnboxon.py","c5"],stdout=subprocess.PIPE).communicate()[0]
		#subprocess.run('sudo','python','./lwturnboxon','c5')
		#return template('<b>Spawned  {{name}}</b>!',name='lwturnboxon')
		
	run(host='0.0.0.0', port=80, debug=True)
	print("in bottlepy after run   ")
		
		
		
