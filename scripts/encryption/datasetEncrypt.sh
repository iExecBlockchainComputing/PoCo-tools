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

	openssl rand -base64 -out $1.keybin 256
	openssl enc -aes-256-cbc -pbkdf2 -in $1 -out $1.enc -kfile $1.keybin
}

function decryptFile()
{
	if [ -e "$1.encrypted" ] && [ -e "$1.key" ]
	then
		echo "Decrypting '$1'"
	else
		echo "Cannot find '$1.encrypt' or '$1.key'. Skipping."
	fi

	openssl enc -aes-256-cbc -pbkdf2 -d -in $1.enc -out $1.recovered -kfile $1.keybin
}

while test $# -gt 0; do
	encryptFile $1
	# decryptFile $1
	shift
done
