#!/usr/bin/bash

curl -H "Content-Type: application/json" -X GET -d '{
	"auth":
	{
		"worker": "0x748e091bf16048cb5103E0E10F9D5a8b7fBDd860",
		"taskid": "0x098f400f58acd32ac4016fe3f95aaf9b3718d3906dd975fe8a65c7648e72954d",
		"enclave": "0xC773B9cd33B20aCd3752BbCFC5b6175f62247593",
		"sign":
		{
			"r": "0x62cb05d1964f835617ad9bd35af087f00ec8fed852577ddf7610b9e7cbf5b0c1",
			"s": "0x5320da9d7823b8c114d5dae3a55c28f2a9abfb3febe7bdfb76d7fafb68ff1cbb",
			"v": 28
			}
	}
}' http://localhost:5000/secure
