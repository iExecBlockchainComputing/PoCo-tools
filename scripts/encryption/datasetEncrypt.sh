#!/bin/bash

function encryptFile()
{
	if [ -e "$1" ]
	then
		echo "Encrypting '$1'"
	else
		echo "'$1' is not a valid file. Skipping."
		return
	fi

	openssl rand -out $1.keybin 32
	openssl enc -aes-256-cbc -pbkdf2 -in $1 -out $1.enc -kfile $1.keybin
	openssl base64 -e -in $1.keybin -out $1.secret
	shred -u $1.keybin
}

function decryptFile()
{
	if [ -e "$1.enc" ] && [ -e "$1.secret" ]
	then
		echo "Decrypting '$1'"
	else
		echo "Cannot find '$1.encrypt' or '$1.key'. Skipping."
	fi

	openssl base64 -d -in $1.secret -out $1.keybin
	openssl enc -aes-256-cbc -pbkdf2 -d -in $1.enc -out $1.recovered -kfile $1.keybin
	shred -u $1.keybin
}

while test $# -gt 0; do
	encryptFile $1
	# decryptFile $1
	shift
done
