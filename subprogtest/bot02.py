#!/usr/bin/python


from __future__ import print_function
import sys
import time
from time import sleep
from bottle import route, run, template, get, post, request, redirect, SimpleTemplate
import subprocess
import signal	
import os
	
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
		proc = subprocess.Popen(['python','./botchild02.py'])
		print ('PARENT       : Pausing before sending signal .....')
		sys.stdout.flush()
		sleep(1)
		print ('PARENT      : Signalling child')
		sys.stdout.flush()
		os.kill(proc.pid, signal.SIGUSR1)
		redirect("/botconfirm?id=%6s" % proc.pid)
		#subprocess.run('sudo','python','./lwturnboxon','c5')
		#return template('<b>Spawned  {{name}}</b>!',name='lwturnboxon')
		
	@route('/botconfirm')
	def botconfirm():
		id = request.query.id
		return_string = "<b>" + "Spawned child, pid is:  " + str(id)
		return return_string
	
	run(host='127.0.0.1', port=8080, debug=True)
	print("in bottlepy after run   ")
		
		
