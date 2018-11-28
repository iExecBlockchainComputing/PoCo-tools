#!/usr/bin/python

import json

path = "build/contracts/IexecUnified.json"

if __name__ == '__main__':
	with open(path) as file:
		bytecode = json.load(file)['deployedBytecode']
		print(bytecode)
		print("Length: {:d}".format(len(bytecode) // 2))
