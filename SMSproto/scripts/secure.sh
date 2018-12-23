#!/usr/bin/bash

curl -H "Content-Type: application/json" -X GET -d '{
	"auth":
	{
		"worker": "0x748e091bf16048cb5103E0E10F9D5a8b7fBDd860",
		"taskid": "0x098f400f58acd32ac4016fe3f95aaf9b3718d3906dd975fe8a65c7648e72954d",
		"enclave": "0x6CDC0e0C0c7b8f409c3ad6734C23677973CA56A3",
		"sign":
		{
			"r": "0x559773b6e19095c731396cae5b90c507bde97425c548b27f4b4fa1ad019b981b",
			"s": "0x17d4fe256a8d6d00780f1ceb2b29fdf2ff3586499abf910274da62d5c6ec6ef9",
			"v": 27
			}
	}
}' http://localhost:5000/secure
