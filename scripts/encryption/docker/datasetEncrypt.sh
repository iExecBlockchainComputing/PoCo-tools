#!/bin/bash

in_path=/input
out_enc_path=/output_enc
out_sec_path=/output_secret

function encryptFile()
{

	if [ -e "$in_path/$1" ]
	then
		echo "Encrypting '$in_path/$1'"
	else
		echo "'$in_path/$1' is not a valid file. Skipping."
		return
	fi
	openssl rand -out $1.keybin 32
	openssl enc -aes-256-cbc -pbkdf2 -in $in_path/$1 -out $out_enc_path/$1.enc -kfile $1.keybin
	openssl base64 -e -in $1.keybin -out $out_sec_path/$1.secret
	shred -u $1.keybin
}

while test $# -gt 0; do
	encryptFile $1
	shift
done
