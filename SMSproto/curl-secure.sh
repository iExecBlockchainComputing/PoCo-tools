#!/usr/bin/bash

curl -H "Content-Type: application/json" -X POST -d '{
	"sign": "0x5f815a46c3b2466c6d8b6f0531812a0fb7405745cd9e7a159712a910389d6793099f4b70a2f0700853c6500be19beb686129d607f95e3889cbf8e0fa28e54c251C",
	"secret": "abcd"
}' http://localhost:5000/contract/0x385fFe1c9Ec3d6a0798eD7a13445Cb2B2de9fd09

curl -H "Content-Type: application/json" -X GET \
http://localhost:5000/contract/0x385fFe1c9Ec3d6a0798eD7a13445Cb2B2de9fd09

curl -H "Content-Type: application/json" -X GET -d '{
	"auth":
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
}' http://localhost:5000/secure
