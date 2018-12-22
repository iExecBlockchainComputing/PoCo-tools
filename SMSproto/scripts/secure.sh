#!/usr/bin/bash

curl -H "Content-Type: application/json" -X GET -d '{
	"auth":
	{
		"worker": "0x748e091bf16048cb5103E0E10F9D5a8b7fBDd860",
		"taskid": "0x098f400f58acd32ac4016fe3f95aaf9b3718d3906dd975fe8a65c7648e72954d",
		"enclave": "0x3e22507d066b25367F1cd2937cdaE747C5da446F",
		"sign":
		{
			"r": "0x50682aa9b1e26b7c13c383d663afce87bcf1ad7107f563d6ca47fe77308debf2",
			"s": "0x03855a35ed2b5fd8bb3b341dcaa021f331907835fdf198437f5f56c5e6152419",
			"v": 28
			}
	}
}' http://localhost:5000/secure
