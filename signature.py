#!/usr/bin/python3
import json
import os
import web3.auto

from py_essentials.hashing import fileChecksum

if __name__ == '__main__':

	taskid  = os.environ.get('TASKID' ) or '0x8b43265c231bd32d1b249c1ce58bf0c77a9ebc6a30da37e961063a073a921e06'
	worker  = os.environ.get('WORKER' ) or '0x748e091bf16048cb5103E0E10F9D5a8b7fBDd860'
	keyfile = os.environ.get('KEYFILE') or '/app/priv_key'

	# DEBUG
	# account = web3.Account.privateKeyToAccount("0x564a9db84969c8159f7aa3d5393c5ecd014fce6a375842a45b12af6677b12407")

	with open(keyfile) as f:
		private = f.read().splitlines()[0]
		account = web3.Account.privateKeyToAccount(private)

	print("Genrating result and consensus.iexec in /iexec ...")
	print(os.system("cp /app/result.txt /iexec/result.txt"))
	print(os.system("cp /app/result.txt /iexec/consensus.iexec"))

	# DEBUG
	# digest    = web3.auto.w3.soliditySha3([ 'string' ], [ 'iExec the wanderer' ]).hex()

	digest    = "0x" + fileChecksum("/iexec/consensus.iexec", "sha256") # hexstring
	hash      = web3.auto.w3.soliditySha3([            'bytes32', 'bytes32' ], [         taskid, digest ])
	seal      = web3.auto.w3.soliditySha3([ 'address', 'bytes32', 'bytes32' ], [ worker, taskid, digest ])
	contrib   = web3.auto.w3.soliditySha3([            'bytes32', 'bytes32' ], [           hash,   seal ])
	signature = web3.auto.w3.eth.sign(account=account.address, data=contrib)
	r         = web3.auto.w3.toHex(signature[ 0:32])
	s         = web3.auto.w3.toHex(signature[32:64])
	v         = web3.auto.w3.toInt(signature[64:65]) + 27

	with open("/tmp/enclaveSig.iexec", 'w') as f:
		json.dump({
			'digest': "0x{}".format(digest),
			'hash':   "0x{}".format(hash.hex()),
			'seal':   "0x{}".format(seal.hex()),
			'sign':   { 'v': v, 'r': "0x{}".format(r), 's': "0x{}".format(s) }
		}, f, ensure_ascii=False)

	print("------ Additional log -------")
	print("ls /iexec/")
	print(os.system("ls /iexec/"))
	print("cat /iexec/enclaveSig.iexec")
	print(os.system("cat /iexec/enclaveSig.iexec"))
