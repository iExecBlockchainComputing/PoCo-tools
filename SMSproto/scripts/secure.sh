#!/usr/bin/bash

curl -H "Content-Type: application/json" -X GET -d '{
	"auth":
	{
		"worker": "0x748e091bf16048cb5103E0E10F9D5a8b7fBDd860",
		"taskid": "0x098f400f58acd32ac4016fe3f95aaf9b3718d3906dd975fe8a65c7648e72954d",
		"enclave": "0xc5c72e94E9721701eeee222a0918aF610D89e0aB",
		"sign":
		{
			"r": "0x50a9708196d246b5cc68b86c80637cb7c110d40dbc6361e1b776e72cf670f6eb",
			"s": "0x2fbcafc020a71cfd4d559638bfcb3dc2735e3c426e8de74d7cf9c212982e7ad0",
			"v": 27
			}
	}
}' http://localhost:5000/secure
