#!/usr/bin/python

import os,sys,time
import logging

def initialize(params):
	print >>sys.__stdout__,"Metric Client initialized with parameters %s" % str(params)

def projection_started(proj):
	print >>sys.__stdout__,"Starting to send data for projection %s" % proj

def projection_finished(proj):
	print >>sys.__stdout__,"Finished sending data for projection %s" % proj

def add_metric(proj,name,value,timestamp):
	print >>sys.__stdout__,"Metric for projection %s - name is %s value is %s timestamp is %s" % (proj,name,value,timestamp)

def done():
	print >>sys.__stdout__,"Metric client done"

