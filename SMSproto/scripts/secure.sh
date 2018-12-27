#!/usr/bin/bash

curl -H "Content-Type: application/json" -X GET -d '{
	"auth":
	{
		"worker": "0x748e091bf16048cb5103E0E10F9D5a8b7fBDd860",
		"taskid": "0x098f400f58acd32ac4016fe3f95aaf9b3718d3906dd975fe8a65c7648e72954d",
		"enclave": "0x3E04a05575731Fbf21d82C72D72a5DD8b20FaF38",
		"sign":
		{
			"r": "0x80530f73ad3c6de390ea3fcc46ace2fa038cdff69a6de0b25772d9fabe4c1bd1",
			"s": "0x00c44ee34460f103f71b6a855f15626ccc2214e147ccede5c745b38fe841cee5",
			"v": 27
			}
	}
}' http://localhost:5000/secure
