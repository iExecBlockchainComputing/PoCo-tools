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

OwnableABI    = json.load(open('/home/amxx/Work/iExec/code/PoCo-dev/build/contracts/OwnableImmutable.json'   ))['abi']
AppABI        = json.load(open('/home/amxx/Work/iExec/code/PoCo-dev/build/contracts/App.json'                ))['abi']
IexecClerkABI = json.load(open('/home/amxx/Work/iExec/code/PoCo-dev/build/contracts/IexecClerkABILegacy.json'))['abi']
IexecHubABI   = json.load(open('/home/amxx/Work/iExec/code/PoCo-dev/build/contracts/IexecHubABILegacy.json'  ))['abi']

def getContract(w3, ABI, address):
	return w3.eth.contract(address=address, abi=ABI, ContractFactoryClass=Contract)

web3       = Web3(HTTPProvider('http://localhost:8545'))
IexecClerk = getContract(web3, IexecClerkABI, address='0x8BE59dA9Bf70e75Aa56bF29A3e55d22e882F91bA')
IexecHub   = getContract(web3, IexecHubABI,   address='0x7C788C2B85E20B4Fa25bd579A6B1D0218D86BDd1')






authorizationJSON = """
	{
		"worker": "0x892407E8E2440DEf7a8854AB0A936D94784d658F",
		"taskid": "0x284cc3a2121190b1db55b92ed7f18e70dadac6183980cd7c7b9d7f9fc5bb83ae",
		"enclave": "0x0000000000000000000000000000000000000000",
		"sign":
		{
			"r": "0x5f815a46c3b2466c6d8b6f0531812a0fb7405745cd9e7a159712a910389d6793",
			"s": "0x099f4b70a2f0700853c6500be19beb686129d607f95e3889cbf8e0fa28e54c25",
			"v": 28
		}
	}
"""






def validateAuthorization(auth):
	# Get task details
	taskid = auth['taskid']
	task   = IexecHub.functions.viewTaskABILegacy(taskid).call()

	# CHECK 1: Task must be Active
	# assert(task[0] == 1)

	# Get deal details
	dealid = task[1]
	deal = IexecClerk.functions.viewDealABILegacy_pt1(dealid).call()          \
	     + IexecClerk.functions.viewDealABILegacy_pt2(dealid).call()

	appaddr        = deal[0]
	datasetaddr    = deal[3]
	workerpooladdr = deal[6]
	scheduler      = deal[7]
	beneficiary    = deal[11]

	# CHECK 2: Authorisation to contribute must be authentic
	hash = web3.soliditySha3([                                                \
		'address',                                                            \
		'bytes32',                                                            \
		'address'                                                             \
	], [                                                                      \
		auth['worker'],                                                       \
		auth['taskid'],                                                       \
		auth['enclave']                                                       \
	])
	signer = web3.eth.account.recoverHash(                                    \
		message_hash=defunct_hash_message(hash),                              \
		vrs=(auth['sign']['v'], auth['sign']['r'], auth['sign']['s'])         \
	)
	assert(signer == scheduler)

	# Get enclave secret
	MREnclave = getContract(                                                  \
		w3      = web3,                                                       \
		ABI     = AppABI,                                                     \
		address = appaddr                                                     \
	).functions.m_appMREnclave().call()
	# TODO: VALIDATE MREnclave of throw AssertionError

	# sys.stderr.write("[DEBUG] task: {}\n".format(task))
	# sys.stderr.write("[DEBUG] deal: {}\n".format(deal))
	# sys.stderr.write("[DEBUG] MREnclave: {}\n".format(MREnclave))

	return datasetaddr, workerpooladdr, beneficiary







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
		return jsonify({                                                      \
			'address': address,                                               \
			'hash':    entry.hash if entry else None                          \
		})

	def post(self, address):
		args   = self.reqparse.parse_args()
		signer = web3.eth.account.recoverHash(                                \
			message_hash=defunct_hash_message(text=args.secret),              \
			signature=args.sign                                               \
		)
		valid  = self.__check(address, signer)
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
	def __check(self, address, signer):
		# return address.lower() == signer.lower()
		return True

# +---------------------------------------------------------------------------+
# |                      For app/dataset encryption key                       |
# +---------------------------------------------------------------------------+

class ContractAPI(AccountAPI):
	def __init__(self):
		super(ContractAPI, self).__init__()

	def __check(self, address, signer):
		# owner  = getContract(                                               \
		# 	ABI=OwnableABI,                                                   \
		# 	address=address                                                   \
		# ).functions.m_owner().call()
		# return owner.lower() == signer.lower()
		return True

# +---------------------------------------------------------------------------+
# |                          For enclave attestation                          |
# +---------------------------------------------------------------------------+
class GenerateAPI(Resource):
	def __init__(self):
		super(GenerateAPI, self).__init__()
		# TODO: handle MREnclave
		# self.reqparse = reqparse.RequestParser()
		# self.reqparse.add_argument('secret', type=str, location='json', required=True)

	def post(self, address):
		account = web3.eth.account.create()
		secret = Secret(                                                      \
			address = account.address,                                        \
			secret  = account.privateKey,                                     \
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
			ids = validateAuthorization(request.json['auth'])
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
	app.run(debug=True)
	db.drop_all()
