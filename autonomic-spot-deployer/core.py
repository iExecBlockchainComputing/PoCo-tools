#!/usr/bin/python3

from apscheduler.schedulers.asyncio    import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking   import BlockingScheduler

# import asyncio
import datetime
import itertools
import json
import urllib.request
import sys
import time

class ActiveOrderbook(object):
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
		return "ActiveOrderbook[{}]".format(self.gateway, self.headers)

class PassiveOrderbook(object):
	def __init__(self, gateway, headers={}):
		self.gateway = gateway
		self.headers = headers

	def get(self, query):
		req = urllib.request.Request(url=self.gateway, headers=self.headers)
		with urllib.request.urlopen(req) as url:
			data = json.loads(url.read().decode())
			return filter(query, data['orders'])


def processOrder(entry):
	sys.stderr.write("Starting to process order {}\n".format(entry['_id']))
	try:
		#######################################################################
		# ROADMAP:                                                            #
		# 1. filter order                                                     #
		# 2. get app order and datasetorder                                   #
		# 3. check blockchain status                                          #
		# 4. sign matching workerpoolorder                                    #
		# 5. update worker needs                                              #
		#######################################################################

		# check matching workerpool
		# check price / policy
		# always got an app
		# → should try multiple until matching
		apporder     = next(apporderbook.get    (query=lambda e: e['_id'] == entry['_id']))
		# if dataset, else null datasetorder
		# → should try multiple until matching
		datasetorder = next(datasetorderbook.get(query=lambda e: e['_id'] == entry['_id']))
		# check blockchain status of orders
		# generate workerpoolorder
		# sign workerpoolorder
		# push orders to clerk
		# provision workers

	except:
		sys.stderr.write("Error processing order {}\n".format(entry['_id']))



if __name__ == '__main__':

	# TODO: configuration

	# setup scheduler
	scheduler = BlockingScheduler()

	# setup order book gateways
	requestorderbook = ActiveOrderbook(
		gateway="https://gateway.iex.ec/orderbook",
		headers={},
		callback=lambda entry: scheduler.add_job(processOrder, trigger='date', args=[ entry ]),
	)
	apporderbook     = PassiveOrderbook(gateway="https://gateway.iex.ec/orderbook", headers={})
	datasetorderbook = PassiveOrderbook(gateway="https://gateway.iex.ec/orderbook", headers={})

	# prefill scheduler
	scheduler.add_job(requestorderbook.tick, id='orderbook-watch', trigger='interval', seconds=1)

	# run daemon
	try:
		scheduler.start()
	except (KeyboardInterrupt, SystemExit):
		pass
	finally:
		pass
