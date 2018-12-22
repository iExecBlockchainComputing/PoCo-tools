#!/usr/bin/python3

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


# Config
# - path
# - gateway
# - hub
# - clerk
# - listen

class iExecBlockchain(object):
	def __init__(self, path, gateway='http://localhost:8545'):
		super(iExecBlockchain, self).__init__()
		self.w3 = Web3(HTTPProvider(gateway))
		self.ABIs = {                                                                 \
			'Ownable':    json.load(open(f'{path}/OwnableImmutable.json'   ))['abi'], \
			'App':        json.load(open(f'{path}/App.json'                ))['abi'], \
			'IexecClerk': json.load(open(f'{path}/IexecClerkABILegacy.json'))['abi'], \
			'IexecHub':   json.load(open(f'{path}/IexecHubABILegacy.json'  ))['abi'], \
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

	def validateAuthorization(self, auth):
		# Get task details
		taskid = auth['taskid']
		task   = self.IexecHub.functions.viewTaskABILegacy(taskid).call()

		# CHECK 1: Task must be Active
		assert(task[0] == 1)

		# Get deal details
		dealid = task[1]
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

		# sys.stderr.write("[DEBUG] task: {}\n".format(task))
		# sys.stderr.write("[DEBUG] deal: {}\n".format(deal))
		# sys.stderr.write("[DEBUG] MREnclave: {}\n".format(MREnclave))

		return datasetaddr, auth['enclave'], beneficiary

# +---------------------------------------------------------------------------+
# |                      For beneficiary encryption key                       |
# +---------------------------------------------------------------------------+
class AccountAPI(Resource):
	def __init__(self):
		super(AccountAPI, self).__init__()
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
		valid  = self.check(address, signer)
		if valid:
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
	def check(self, address, signer):
		return address.lower() == signer.lower()

# +---------------------------------------------------------------------------+
# |                      For app/dataset encryption key                       |
# +---------------------------------------------------------------------------+

class ContractAPI(AccountAPI):
	def __init__(self):
		super(ContractAPI, self).__init__()

	def check(self, address, signer):
		owner  = iexecblockchain.getContract(                                 \
			address=address,                                                  \
			abiname='Ownable',                                                \
		).functions.m_owner().call()
		return owner.lower() == signer.lower()

# +---------------------------------------------------------------------------+
# |                          For enclave attestation                          |
# +---------------------------------------------------------------------------+
class GenerateAPI(Resource):
	def __init__(self):
		super(GenerateAPI, self).__init__()
		# TODO: handle MREnclave
		# self.reqparse = reqparse.RequestParser()
		# self.reqparse.add_argument('secret', type=str, location='json', required=True)

	def get(self, address):
		account = iexecblockchain.w3.eth.account.create()
		secret = Secret(                                                      \
			address = account.address,                                        \
			secret  = iexecblockchain.w3.toHex(account.privateKey),           \
			hash    = None                                                    \
		)
		db.session.merge(secret)
		db.session.commit()
		return jsonify({ 'address': account.address })

# +---------------------------------------------------------------------------+
# |                                                                           |
# +---------------------------------------------------------------------------+
class SecureAPI(Resource):
	def __init__(self):
		super(SecureAPI, self).__init__()
		# TODO: RequestParser for auth

	def get(self):
		try:
			ids = iexecblockchain.validateAuthorization(request.json['auth'])
			Kd = Secret.query.filter_by(address=ids[0]).first()
			Ke = Secret.query.filter_by(address=ids[1]).first()
			Kb = Secret.query.filter_by(address=ids[2]).first()
			return jsonify({                                                  \
				'Kd': Kd.jsonify() if Kd else None,                           \
				'Ke': Ke.jsonify() if Ke else None,                           \
				'Kb': Kb.jsonify() if Kb else None                            \
			})
		except AssertionError:
			return jsonify({ 'error': 'access denied' })





iexecblockchain = iExecBlockchain(path='/home/amxx/Work/iExec/code/PoCo-dev/build/contracts')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/sms.db'

db = SQLAlchemy(app)

api = Api(app)
api.add_resource(AccountAPI,  '/account/<string:address>',  endpoint = 'account' ) # address: account
api.add_resource(ContractAPI, '/contract/<string:address>', endpoint = 'contract') # address: contract
api.add_resource(GenerateAPI, '/generate/<string:address>', endpoint = 'generate')
api.add_resource(SecureAPI,   '/secure',                    endpoint = 'secure'  )

@app.route('/', methods=['GET'])
def index(): return "This is a test SMS service"

@app.errorhandler(404)
def not_found(error): return make_response(jsonify({'error': 'Not found'}), 404)


class Secret(db.Model):
	address = db.Column(db.String(66), primary_key=True)
	secret  = db.Column(db.TEXT,       unique=False, nullable=True)
	hash    = db.Column(db.String(10), unique=False, nullable=True)

	def jsonify(self):
		return { 'address': self.address, 'secret': self.secret }







if __name__ == '__main__':
	db.create_all()
	app.run(debug=False)
	db.drop_all()
