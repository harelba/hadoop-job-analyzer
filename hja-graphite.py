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

def add_projection_metric(proj,name,value,timestamp):
	add_metric(name,value,timestamp)

def add_metric(name,value,timestamp):
	global metrics_to_send
	metrics_to_send.append((name,value,timestamp))

def done():
	global metrics_to_send
	_do_send(metrics_to_send)

def _do_send(metrics_tuples):
	global graphite_server,graphite_port

	data_list = []
	for name,value,timestamp in metrics_tuples:
		data = "%(name)s %(value)s %(timestamp)s" % vars()
		data_list.append(data)

	data = "\n".join(data_list)
	data += "\n"
	
	try:
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.connect((graphite_server,graphite_port))
		sock.send(data)
		sock.close()
	except Exception,e:
		print >>sys.__stderr__,"Error trying to send metric data %s " % tb.format_exc()
		logging.error("Error trying to send metric data %s " % tb.format_exc())
