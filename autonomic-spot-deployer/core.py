#!/usr/bin/python3

from apscheduler.schedulers.blocking import BlockingScheduler
from web3                            import Web3, HTTPProvider
from web3.contract                   import Contract, ConciseContract

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
		return web3.eth.contract(address=address, abi=json.load(file)['abi'], ContractFactoryClass=Contract)


class EventListener(object):
	def __init__(self, event):
		self.evfilter = event.createFilter(fromBlock=0)
		# fromBlock='latest'
		# argument_filters={'arg1':10}
	def getNew(self):
		return self.evfilter.get_all_entries()
	def tick(self):
		print("tick: {}".format(self.getNew()))



if __name__ == '__main__':
	# TODO: configuratione

	# setup scheduler
	scheduler = BlockingScheduler()

	# # setup order book gateways
	# requestorderbook = orderbook.ActiveListener(
	# gateway="https://gateway.iex.ec/orderbook",
	# headers={},
	# callback=lambda entry: scheduler.add_job(processOrder, trigger='date', args=[ entry ]),
	# )
	# apporderbook     = orderbook.PassiveListener(gateway="https://gateway.iex.ec/orderbook", headers={})
	# datasetorderbook = orderbook.PassiveListener(gateway="https://gateway.iex.ec/orderbook", headers={})








	web3 = Web3(HTTPProvider('http://localhost:8545'))
	# account = '0x2D29bfBEc903479fe4Ba991918bAB99B494f2bEf'

	IexecClerkInstance = getContract(path='contracts/IexecClerk.json', address='0x8BE59dA9Bf70e75Aa56bF29A3e55d22e882F91bA')
	print("clerk: {}".format(IexecClerkInstance.address))
	print("token: {}".format(IexecClerkInstance.functions.token().call()))
	print("hub  : {}".format(IexecClerkInstance.functions.iexechub().call()))

	# orderfactory = eip712.Factory(web3=web3, domain=eip712.Domain(
	# 	name              = "iExecODB",
	# 	version           = "3.0-alpha",
	# 	chainId           = 1544020727674,
	# 	verifyingContract = IexecClerkInstance.address
	# ))
	# print(web3.toHex(orderfactory.EIP712DOMAIN_SEPARATOR))
	# print(web3.toHex(IexecClerkInstance.functions.EIP712DOMAIN_SEPARATOR().call()))


	topic1 = web3.sha3(text="OrdersMatched(bytes32,bytes32,bytes32,bytes32,bytes32,uint256)").hex()
	topic2 = web3.sha3(text="SchedulerNotice(address,bytes32)").hex()
	print("address:", IexecClerkInstance.address)
	print("topic 1:", topic1)
	print("topic 2:", topic2)

	evfilter = web3.eth.filter({
		# "address": IexecClerkInstance.address,
		# "topics": [ topic1 ]
	})

	# evfilter = IexecClerkInstance.events.OrdersMatched.createFilter(fromBlock='latest')


	def tick():
		print("-")
		for ev in evfilter.get_all_entries():
			print("[EVENT@{blockNumber}] from: {address} topic: {topics[0]}".format(**ev))



	# prefill scheduler
	# scheduler.add_job(requestorderbook.tick, id='orderbook-watch', trigger='interval', seconds=1)
	# scheduler.add_job(evlistener1.tick, id='event-watch-1', trigger='interval', seconds=1)
	scheduler.add_job(tick, id='event-watch', trigger='interval', seconds=1)

	# run daemon
	try:
		scheduler.start()
	except (KeyboardInterrupt, SystemExit):
		pass
	finally:
		pass
