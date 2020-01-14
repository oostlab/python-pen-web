#!/usr/bin/env
# Changed for python3
import sys

def request(context, flow):
	f = open('httplogs.txt', 'a+')
	f.write(flow.request.url + '\n')	
	f.close()
