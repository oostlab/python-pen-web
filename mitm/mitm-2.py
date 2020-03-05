#!/usr/bin/env
# Changed for python3
import sys

def request(context, flow):
	q = flow.request.get_query()
	if q:
		q["isadmin"] = ["True"]
		flow.request.set_query(q)
