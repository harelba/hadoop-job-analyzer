#!/usr/bin/python

import logging
import os,sys,time
import socket
from datetime import datetime
import traceback as tb

graphite_server = None
graphite_port = None

metrics_to_send = []

def initialize(params):
	global graphite_server
	global graphite_port
	try:
		graphite_server = params['server']
		graphite_port = int(params['port'])
	except Exception,e:
		print >>sys.__stderr__,"Graphite metric client requires server and port parameters"
		logging.error("Graphite metric client requires server and port parameters")
		raise e

def projection_started(proj):
	pass

def projection_finished(proj):
	pass

def add_metric(proj,name,value,timestamp):
	global metrics_to_send
	metrics_to_send.append((name,value,timestamp))

def done():
	global graphite_server,graphite_port
	global metrics_to_send

	data_list = []
	for name,value,timestamp in metrics_to_send:
		data = "%(name)s %(value)s %(timestamp)s" % vars()
		data_list.append(data)

	data = "\n".join(data_list)
	
	try:
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.connect((graphite_server,graphite_port))
		sock.send(data)
		sock.close()
	except Exception,e:
		print >>sys.__stderr__,"Error trying to send metric data %s " % tb.format_exc()
		logging.error("Error trying to send metric data %s " % tb.format_exc())
    

