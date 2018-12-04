#!/usr/bin/python3

import collections

Domain          = collections.namedtuple('Domain',          [ 'name', 'version', 'chainId', 'verifyingContract' ])
AppOrder        = collections.namedtuple('AppOrder',        [ 'app', 'appprice', 'volume', 'tag', 'datasetrestrict', 'workerpoolrestrict', 'requesterrestrict', 'salt' ])
DatasetOrder    = collections.namedtuple('DatasetOrder',    [ 'dataset', 'datasetprice', 'volume', 'tag', 'apprestrict', 'workerpoolrestrict', 'requesterrestrict', 'salt' ])
WorkerpoolOrder = collections.namedtuple('WorkerpoolOrder', [ 'workerpool', 'workerpoolprice', 'volume', 'tag', 'category', 'trust', 'apprestrict', 'datasetrestrict', 'requesterrestrict', 'salt' ])
RequestOrder    = collections.namedtuple('RequestOrder',    [ 'app', 'appmaxprice', 'dataset', 'datasetmaxprice', 'workerpool', 'workerpoolmaxprice', 'requester', 'volume', 'tag', 'category', 'trust', 'beneficiary', 'callback', 'params', 'salt' ])

EIP712DOMAIN_TYPEHASH    = '0x8b73c3c69bb8fe3d512ecc4cf759cc79239f7b179b0ffacaa9a75d522b39400f'
APPORDER_TYPEHASH        = '0x7ec080e12d68143b6f3cbfcc951a0af368f44b0317bf88e47a6deb61360f467a'
DATASETORDER_TYPEHASH    = '0x5a29cc8df638f0050902f3d568d4f66123c5aa434ed1b7f7448e3f8698ae9887'
WORKERPOOLORDER_TYPEHASH = '0xc35d0ed8a07a66003ec762099c137d24991e5d74651822289074551ed1d9f9ae'
REQUESTORDER_TYPEHASH    = '0xf56ae5843d5bed3b1e1c005f4793303f8b9525f9f40189b8d29c21c2984a1ce4'

class Factory(object):
	def __init__(self, web3, domain):
		self.web3                   = web3
		self.EIP712DOMAIN_SEPARATOR = self.DomainStructHash(domain)

	def DomainStructHash(self, domain):
		return self.web3.soliditySha3([
			'bytes32',
			'bytes32',
			'bytes32',
			'uint256',
			'address',
		],[
			EIP712DOMAIN_TYPEHASH,
			self.web3.sha3(text=domain.name   ),
			self.web3.sha3(text=domain.version),
			domain.chainId,
			domain.verifyingContract,
		])

	def AppOrderStructHash(self, apporder):
		return self.web3.soliditySha3([
			'bytes32',
			'address',
			'uint256',
			'uint256',
			'uint256',
			'address',
			'address',
			'address',
			'bytes32',
		],[
			APPORDER_TYPEHASH,
			apporder.app,
			apporder.appprice,
			apporder.volume,
			apporder.tag,
			apporder.datasetrestrict,
			apporder.workerpoolrestrict,
			apporder.requesterrestrict,
			apporder.salt,
		])

	def DatasetOrderStructHash(self, datasetorder):
		return self.web3.soliditySha3([
			'bytes32',
			'address',
			'uint256',
			'uint256',
			'uint256',
			'address',
			'address',
			'address',
			'bytes32',
		],[
			DATASETORDER_TYPEHASH,
			datasetorder.dataset,
			datasetorder.datasetprice,
			datasetorder.volume,
			datasetorder.tag,
			datasetorder.apprestrict,
			datasetorder.workerpoolrestrict,
			datasetorder.requesterrestrict,
			datasetorder.salt,
		])

	def WorkerpoolOrderStructHash(self, workerpoolorder):
		return self.web3.soliditySha3([
			'bytes32',
			'address',
			'uint256',
			'uint256',
			'uint256',
			'uint256',
			'uint256',
			'address',
			'address',
			'address',
			'bytes32',
		],[
			WORKERPOOLORDER_TYPEHASH,
			workerpoolorder.workerpool,
			workerpoolorder.workerpoolprice,
			workerpoolorder.volume,
			workerpoolorder.tag,
			workerpoolorder.category,
			workerpoolorder.trust,
			workerpoolorder.apprestrict,
			workerpoolorder.datasetrestrict,
			workerpoolorder.requesterrestrict,
			workerpoolorder.salt,
		])

	def RequestOrderStructHash(self, requestorder):
		return self.web3.soliditySha3([
			'bytes32',
			'address',
			'uint256',
			'address',
			'uint256',
			'address',
			'uint256',
			'address',
			'uint256',
			'uint256',
			'uint256',
			'uint256',
			'address',
			'address',
			'bytes32',
			'bytes32',
		],[
			REQUESTORDER_TYPEHASH,
			requestorder.app,
			requestorder.appmaxprice,
			requestorder.dataset,
			requestorder.datasetmaxprice,
			requestorder.workerpool,
			requestorder.workerpoolmaxprice,
			requestorder.requester,
			requestorder.volume,
			requestorder.tag,
			requestorder.category,
			requestorder.trust,
			requestorder.beneficiary,
			requestorder.callback,
			self.web3.sha3(text=requestorder.params),
			requestorder.salt,
		])
