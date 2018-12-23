#!/usr/bin/bash

curl -H "Content-Type: application/json" -X POST -d '{
	"sign": "0x24cc47ff51df3ee33b69062829d11370e801b010b4f4a8246ace99625080a4b80cd9ed492c649f22d7dd8f79a7538e74c46f5d54c22e1c749bc38e643f06d3e300",
	"secret": "abcdef"
}' http://localhost:5000/secret/0x385fFe1c9Ec3d6a0798eD7a13445Cb2B2de9fd09
