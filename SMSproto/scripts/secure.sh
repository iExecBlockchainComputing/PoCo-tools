#!/usr/bin/bash

curl -H "Content-Type: application/json" -X GET -d '{
	"auth":
	{
		"worker": "0x748e091bf16048cb5103E0E10F9D5a8b7fBDd860",
		"taskid": "0x098f400f58acd32ac4016fe3f95aaf9b3718d3906dd975fe8a65c7648e72954d",
		"enclave": "0x7943E75A48FEf0376CCDcdda87fea71a4A9730C4",
		"sign":
		{
			"r": "0x9662f9516fada7ca4e19263b0206aee86265a3bf9cf91c0622b11d26341ce4e0",
			"s": "0x3d9a26a9dd3d28e2e04178a8c9af055b8b50faaf5b0913d1d1737cf09bca3a73",
			"v": 28
			}
	}
}' http://localhost:5000/secure
