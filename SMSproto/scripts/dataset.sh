#!/usr/bin/bash

curl -H "Content-Type: application/json" -X POST -d '{
	"sign": "0x5f815a46c3b2466c6d8b6f0531812a0fb7405745cd9e7a159712a910389d6793099f4b70a2f0700853c6500be19beb686129d607f95e3889cbf8e0fa28e54c251C",
	"secret": "abcdef"
}' http://localhost:5000/contract/0x385fFe1c9Ec3d6a0798eD7a13445Cb2B2de9fd09
