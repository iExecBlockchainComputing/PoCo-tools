#!/usr/bin/bash

curl -H "Content-Type: application/json" -X GET -d '{
	"auth":
	{
		"worker": "0x748e091bf16048cb5103E0E10F9D5a8b7fBDd860",
		"taskid": "0x8fc4bd2dcdae6f572324a62f61383afc0849bd15636c5231bebb31b50c3d11b1",
		"enclave": "0x7943E75A48FEf0376CCDcdda87fea71a4A9730C4",
		"sign":
		{
			"r": "0x0efa8b2fd745abc71cb2f0ab94e34e9089322e6324226e40ae709125c2abd47a",
			"s": "0x786f148a4fadd26c1db0ef3a7a59b78918475eda773262c147fe7fd97cb82f6c",
			"v": 27
			}
	}
}' http://localhost:5000/secure
