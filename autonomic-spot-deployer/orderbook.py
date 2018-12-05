#!/usr/bin/python3

import datetime
import json
import urllib.request
import sys


class ActiveListener(object):
	def __init__(self, gateway, headers={}, callback=None):
		self.gateway  = gateway
		self.headers  = headers
		self.viewed   = set()
		self.callback = callback

	def get(self):
		req = urllib.request.Request(url=self.gateway, headers=self.headers)
		with urllib.request.urlopen(req) as url:
			data = json.loads(url.read().decode())
			return data['orders']

	def tick(self):
		sys.stderr.write("[{:%Y%m%d-%H%M%S}] {} tick\n".format(datetime.datetime.now(), self))
		for entry in self.get():
			if 'orderHash' not in entry:
				entry['orderHash'] = hash(frozenset(entry.items()))
			if entry['orderHash'] not in self.viewed:
				self.viewed.add(entry['orderHash'])
				self.callback(entry)

	def __repr__(self):
		return "ActiveListener[{}]".format(self.gateway, self.headers)

class PassiveListener(object):
	def __init__(self, gateway, headers={}):
		self.gateway = gateway
		self.headers = headers

	def get(self):
		req = urllib.request.Request(url=self.gateway, headers=self.headers)
		with urllib.request.urlopen(req) as url:
			data = json.loads(url.read().decode())
			return data['orders']
