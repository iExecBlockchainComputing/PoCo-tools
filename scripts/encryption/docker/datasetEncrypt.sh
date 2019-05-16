#!/bin/bash

in_path=/input
out_enc_path=/output_enc
out_sec_path=/output_secret

function encryptFile()
{

	if [ -e "$in_path/$1" ]
	then
		echo "Encrypting $1"
	else
		(>&2 echo "$1 is not a valid file.")
		exit 1
	fi
	openssl rand -out $1.keybin 32
	openssl enc -aes-256-cbc -pbkdf2 -in $in_path/$1 -out $out_enc_path/$1.enc -kfile $1.keybin
	echo "Generated key file $1.secret for dateset $1"
	openssl base64 -e -in $1.keybin -out $out_sec_path/$1.secret
	shred -u $1.keybin
	echo "Generated encrypted dataset $1.enc from dateset $1"
}

while test $# -gt 0; do
	encryptFile $1
	shift
done
