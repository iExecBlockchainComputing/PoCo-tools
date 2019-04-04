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

	dd if=/dev/urandom of=$1.tmpkey bs=512 count=1
	openssl enc -aes-256-cbc -pbkdf2 -in $1 -out $1.encrypted -kfile $1.tmpkey
	base64 $1.tmpkey > $1.key
	rm $1.tmpkey
}

function decryptFile()
{
	if [ -e "$1.encrypted" ] && [ -e "$1.key" ]
	then
		echo "Decrypting '$1'"
	else
		echo "Cannot find '$1.encrypt' or '$1.key'. Skipping."
	fi

	base64 -d $1.key > $1.tmpkey
	openssl enc -aes-256-cbc -pbkdf2 -d -in $1.encrypted -out $1.recovered -kfile $1.tmpkey
	rm $1.tmpkey
}

while test $# -gt 0; do
	encryptFile $1
	shift
done
