#!/usr/bin/python3

# import argparser
import json
import hashlib
import io
import sys

from web3                 import Web3, HTTPProvider
from web3.contract        import Contract, ConciseContract
from eth_account.messages import defunct_hash_message
from flask                import Flask, jsonify, make_response, request
from flask_restful        import Api, Resource, reqparse
from flask_sqlalchemy     import SQLAlchemy


class iExecBlockchain(object):
	def __init__(self, path):
		super(iExecBlockchain, self).__init__()
		self.w3 = Web3(HTTPProvider('http://localhost:8545'))
		self.ABIs = {                                                              \
			'Ownable':    json.load(open(f'{path}/OwnableImmutable.json'))['abi'], \
			'App':        json.load(open(f'{path}/App.json'             ))['abi'], \
			'IexecClerk': json.load(open(f'{path}/IexecClerk.json'      ))['abi'], \
			'IexecHub':   json.load(open(f'{path}/IexecHub.json'        ))['abi'], \
		}
		self.IexecClerk = self.getContract(                                   \
			address='0x8BE59dA9Bf70e75Aa56bF29A3e55d22e882F91bA',             \
			abiname='IexecClerk',                                             \
		)
		self.IexecHub = self.getContract(                                     \
			address='0x7C788C2B85E20B4Fa25bd579A6B1D0218D86BDd1',             \
			abiname='IexecHub',                                               \
		)

	def getContract(self, address, abiname):
		return self.w3.eth.contract(                                          \
			address=address,                                                  \
			abi=self.ABIs[abiname],                                           \
			ContractFactoryClass=Contract,                                    \
		)

	def validateAndGetKeys(self, auth):
		# Get task details
		taskid = auth['taskid']
		# task1 = self.IexecHub.functions.viewTask(taskid).call()
		# print(task1)
		task = self.IexecHub.functions.viewTaskABILegacy(taskid).call()

		# CHECK 1: Task must be Active
		assert(task[0] == 1)

		# Get deal details
		dealid = task[1]
		# deal1 = self.IexecClerk.functions.viewDeal(dealid).call()
		# print(deal1)
		deal = self.IexecClerk.functions.viewDealABILegacy_pt1(dealid).call() \
		     + self.IexecClerk.functions.viewDealABILegacy_pt2(dealid).call()

		appaddr        = deal[0]
		datasetaddr    = deal[3]
		scheduler      = deal[7]
		beneficiary    = deal[11]

		# CHECK 2: Authorisation to contribute must be authentic
		hash = self.w3.soliditySha3([                                         \
			'address',                                                        \
			'bytes32',                                                        \
			'address'                                                         \
		], [                                                                  \
			auth['worker'],                                                   \
			auth['taskid'],                                                   \
			auth['enclave']                                                   \
		])
		signer = self.w3.eth.account.recoverHash(                             \
			message_hash=defunct_hash_message(hash),                          \
			vrs=(auth['sign']['v'], auth['sign']['r'], auth['sign']['s'])     \
		)
		assert(signer == scheduler)

		# Get enclave secret
		MREnclave = self.getContract(                                         \
			address=appaddr,                                                  \
			abiname='App',                                                    \
		)
		# TODO: VALIDATE MREnclave of throw AssertionError

		Kd = Secret.query.filter_by (address=datasetaddr                 ).first()
		Ke = KeyPair.query.filter_by(address=auth['enclave'], app=appaddr).first()
		Kb = Secret.query.filter_by (address=beneficiary                 ).first()
		return Kd, Ke, Kb

# +---------------------------------------------------------------------------+
# |                      For beneficiary encryption key                       |
# +---------------------------------------------------------------------------+
class SecretAPI(Resource):
	def __init__(self):
		super(SecretAPI, self).__init__()
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('secret', type=str, location='json', required=True)
		self.reqparse.add_argument('sign',   type=str, location='json', required=True)


	def get(self, address):
		entry = Secret.query.filter_by(address=address).first()
		if entry:
			return jsonify({ 'address': address, 'hash': entry.hash })
		else:
			return jsonify({})

	def post(self, address):
		args   = self.reqparse.parse_args()
		signer = iexecblockchain.w3.eth.account.recoverHash(                  \
			message_hash=defunct_hash_message(text=args.secret),              \
			signature=args.sign                                               \
		)
		if self.__check(address, signer):
			secret = Secret(                                                  \
				address = address,                                            \
				secret  = args.secret,                                        \
				hash    = hashlib.sha256(args.secret.encode()).hexdigest()    \
			)
			db.session.merge(secret)
			db.session.commit()
			return jsonify({                                                  \
				'address': secret.address,                                    \
				'hash':    secret.hash,                                       \
			})
		else:
			return jsonify({                                                  \
				'error': 'invalid signature',                                 \
			})

	def __check(self, address, signer):
		try:
			if signer.lower() == address.lower():
				return True
			else:
				owner = iexecblockchain.getContract(                          \
					address=address,                                          \
					abiname='Ownable',                                        \
				).functions.m_owner().call()
				return signer.lower() == owner.lower()
		except:
			return False

# +---------------------------------------------------------------------------+
# |                          For enclave attestation                          |
# +---------------------------------------------------------------------------+
class GenerateAPI(Resource):
	def __init__(self):
		super(GenerateAPI, self).__init__()

	def get(self, address):
		account = iexecblockchain.w3.eth.account.create()
		keypair  = KeyPair(                                                   \
			address = account.address,                                        \
			private = iexecblockchain.w3.toHex(account.privateKey),           \
			app     = address                                                 \
		)
		db.session.merge(keypair)
		db.session.commit()
		return jsonify({ 'address': account.address })

class VerifyAPI(Resource):
	def __init__(self):
		super(VerifyAPI, self).__init__()

	def get(self, address):
		entry = KeyPair.query.filter_by(address=address).first()
		if entry:
			return jsonify({ 'address': address, 'app': entry.app })
		else:
			return jsonify({})

# +---------------------------------------------------------------------------+
# |                      For secret retreival by enclave                      |
# +---------------------------------------------------------------------------+
class SecureAPI(Resource):
	def __init__(self):
		super(SecureAPI, self).__init__()
		# TODO: RequestParser for auth

	def get(self):
		try:
			Kd, Ke, Kb = iexecblockchain.validateAndGetKeys(request.json['auth'])
			return jsonify({                                                  \
				'Kd': Kd.jsonify() if Kd else None,                           \
				'Ke': Ke.jsonify() if Ke else None,                           \
				'Kb': Kb.jsonify() if Kb else None                            \
			})
		except AssertionError:
			return jsonify({ 'error': 'access denied' })



# ENVIRONMENT VARIABLES
app = Flask(__name__)
db  = SQLAlchemy(app)
api = Api(app)
api.add_resource(SecretAPI,   '/secret/<string:address>',               endpoint = 'secret'  ) # address: account or ressource SC
api.add_resource(GenerateAPI, '/attestation/generate/<string:address>', endpoint = 'generate') # address: appid
api.add_resource(VerifyAPI,   '/attestation/verify/<string:address>',   endpoint = 'verify'  ) # address: enclaveChallenge
api.add_resource(SecureAPI,   '/secure',                                endpoint = 'secure'  )

@app.route('/', methods=['GET'])
def index(): return "This is a test SMS service"

@app.errorhandler(404)
def not_found(error): return make_response(jsonify({'error': 'Not found'}), 404)

# +---------------------------------------------------------------------------+
# |        DB MODELS: generic secret format for accounts and contracts        |
# +---------------------------------------------------------------------------+
class Secret(db.Model):
	address = db.Column(db.String(42), primary_key=True)
	secret  = db.Column(db.TEXT,       unique=False, nullable=True)
	hash    = db.Column(db.String(64), unique=False, nullable=True)

	def jsonify(self):
		return { 'address': self.address, 'secret': self.secret }

# +---------------------------------------------------------------------------+
# |            DB MODELS: ethereum keypair for enclave attestation            |
# +---------------------------------------------------------------------------+
class KeyPair(db.Model):
	address = db.Column(db.String(42), primary_key=True)
	private = db.Column(db.String(66), unique=True,  nullable=False)
	app     = db.Column(db.String(42), unique=False, nullable=False)

	def jsonify(self):
		return { 'address': self.address, 'private': self.private }









if __name__ == '__main__':

	# TODO: argparser
	# Config
	# - listen
	# - gateway
	# - database
	# - contracts
	# - hub
	# - clerk

	iexecblockchain = iExecBlockchain(path='/home/amxx/Work/iExec/code/PoCo-dev/build/contracts')
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/sms.db'

	db.create_all()
	app.run(debug=False)
	# db.drop_all()
