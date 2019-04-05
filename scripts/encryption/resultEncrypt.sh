#!/bin/bash

function encrypt()
{
	openssl rand -base64 -out $1.keybin 256
	openssl enc -aes-256-cbc -pbkdf2 -kfile $1.keybin -in $1 -out $1.enc
	openssl rsautl -encrypt -inkey key.pub -pubin -in $1.keybin -out $1.keybin.enc
	tar -cf $1.tar $1.enc $1.keybin.enc
	shred -u $1.enc $1.keybin $1.keybin.enc
}

function decrypt()
{
	tar -xf $1.tar
	openssl rsautl -decrypt -inkey key.pem -in $1.keybin.enc -out $1.keybin
	openssl enc -d -aes-256-cbc -pbkdf2 -kfile $1.keybin -in $1.enc -out $1.recovered
	shred -u $1.enc $1.keybin $1.keybin.enc
}


while test $# -gt 0; do
	encrypt $1
	# decrypt $1
	shift
done
