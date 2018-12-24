#!/usr/bin/bash

curl -H "Content-Type: application/json" -X GET -d '{
	"auth":
	{
		"worker": "0x748e091bf16048cb5103E0E10F9D5a8b7fBDd860",
		"taskid": "0x098f400f58acd32ac4016fe3f95aaf9b3718d3906dd975fe8a65c7648e72954d",
		"enclave": "0x715a60A32d99677020AB3c14987F947Ae5962A4C",
		"sign":
		{
			"r": "0x9894dad1a898a6ab699feddb587781e99deee374d4e0ee9f22d43ecd2ce3db10",
			"s": "0x0a01c4d18ae305e15d48a7fb15e03409de699a46ed3afb15ce4192ac778085bb",
			"v": 27
			}
	}
}' http://localhost:5000/secure
