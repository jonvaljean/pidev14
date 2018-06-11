#!/usr/bin/python


from __future__ import print_function
import sys
import time
from time import sleep
from bottle import route, run, template, get, post, request, redirect, SimpleTemplate
import subprocess
	
	#run the programm
if __name__ == "__main__":

	@route('/bottest')
	def bottest():
		return'''
			<form action="/spawn" method="POST">
				<br>
				<input value="Test" type="submit" />
			</form>
		'''
		
		
	@route('/spawn', method="POST")
	def spawn():
		subprocess.Popen(['python','./botchild.py'],stdout=subprocess.PIPE)
		redirect("botconfirm")
		#subprocess.run('sudo','python','./lwturnboxon','c5')
		#return template('<b>Spawned  {{name}}</b>!',name='lwturnboxon')
		
	@route('/botconfirm')
	def botconfirm():
		return '<b>Spawned child'
	
	run(host='0.0.0.0', port=8080, debug=True)
	print("in bottlepy after run   ")
		
		
