#!/usr/bin/python3

# from apscheduler.schedulers.asyncio  import AsyncIOScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

from web3 import Web3, HTTPProvider

# import asyncio
# import itertools
import json
import sys


import eip712
import orderbook


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
		# → should cache
		apporder = next(filter(lambda e: e['_id'] == entry['_id'], apporderbook.get()))

		# if dataset, else null datasetorder
		# → should cache
		if True:
			datasetorder = next(filter(lambda e: e['_id'] == entry['_id'], datasetorderbook.get()))
		else:
			datasetorder = None

		# check blockchain status of orders
		# generate workerpoolorder
		# sign workerpoolorder
		# push orders to clerk
		# provision workers

	except:
		sys.stderr.write("Error processing order {}\n".format(entry['_id']))




def getContract(path, address):
	with open(path) as file:
		return web3.eth.contract(address=address, abi=json.load(file)['abi'])

if __name__ == '__main__':

	# account = '0x2D29bfBEc903479fe4Ba991918bAB99B494f2bEf'

	web3 = Web3(HTTPProvider('http://localhost:8545'))

	IexecClerkInstance = getContract(path='contracts/IexecClerk.json', address='0x8BE59dA9Bf70e75Aa56bF29A3e55d22e882F91bA')
	print("clerk: {}".format(IexecClerkInstance.address))
	print("token: {}".format(IexecClerkInstance.functions.token().call()))
	print("hub  : {}".format(IexecClerkInstance.functions.iexechub().call()))

	orderfactory = eip712.Factory(web3=web3, domain=eip712.Domain(
		name              = "iExecODB",
		version           = "3.0-alpha",
		chainId           = 1543945848970,
		verifyingContract = IexecClerkInstance.address
	))

	print(web3.toHex(orderfactory.EIP712DOMAIN_SEPARATOR))
	print(web3.toHex(IexecClerkInstance.functions.EIP712DOMAIN_SEPARATOR().call()))

	# exit(0)




	# TODO: configuratione

	# setup scheduler
	scheduler = BlockingScheduler()

	# setup order book gateways
	requestorderbook = orderbook.ActiveOrderbook(
		gateway="https://gateway.iex.ec/orderbook",
		headers={},
		callback=lambda entry: scheduler.add_job(processOrder, trigger='date', args=[ entry ]),
	)
	apporderbook     = orderbook.PassiveOrderbook(gateway="https://gateway.iex.ec/orderbook", headers={})
	datasetorderbook = orderbook.PassiveOrderbook(gateway="https://gateway.iex.ec/orderbook", headers={})

	# prefill scheduler
	scheduler.add_job(requestorderbook.tick, id='orderbook-watch', trigger='interval', seconds=1)

	# run daemon
	try:
		scheduler.start()
	except (KeyboardInterrupt, SystemExit):
		pass
	finally:
		pass
