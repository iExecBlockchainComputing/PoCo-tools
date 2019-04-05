#!/bin/bash

# function encrypt()
# {
# 	openssl rand -base64 -out $1.keybin 256
# 	openssl enc -aes-256-cbc -pbkdf2 -kfile $1.keybin -in $1 -out $1.enc
# 	openssl rsautl -encrypt -inkey key.pub -pubin -in $1.keybin -out $1.keybin.enc
# 	tar -cf $1.tar $1.enc $1.keybin.enc
# 	shred -u $1.enc $1.keybin $1.keybin.enc
# }
#
# function decrypt()
# {
# 	tar -xf $1.tar
# 	openssl rsautl -decrypt -inkey key.pem -in $1.keybin.enc -out $1.keybin
# 	openssl enc -d -aes-256-cbc -pbkdf2 -kfile $1.keybin -in $1.enc -out $1.recovered
# 	shred -u $1.enc $1.keybin $1.keybin.enc
# }

RSA_KEY=".tee-secrets/beneficiary/0x4d65930f53da6C277F1769170Df69d772a492008_key"

ROOT_FOLDER="iexec_out"
ENC_RESULT_FILE="result.zip.aes"
ENC_KEY_FILE="encrypted_key"
TMP_KEY_FILE=".tmp-key"

function encrypt()
{
	mkdir ${ROOT_FOLDER}
	openssl rand -out ${TMP_KEY_FILE} 16
	openssl enc -aes-128-cbc -pbkdf2 -kfile ${TMP_KEY_FILE} -in $1 -out ${ROOT_FOLDER}/${ENC_RESULT_FILE}
	openssl rsautl -encrypt -oaep -inkey ${RSA_KEY}.pub -pubin -in ${TMP_KEY_FILE} -out ${ROOT_FOLDER}/${ENC_KEY_FILE}
	zip -r ${ROOT_FOLDER} ${ROOT_FOLDER}

	shred -u ${TMP_KEY_FILE}
	rm -r ${ROOT_FOLDER}
}

while test $# -gt 0; do
	encrypt $1
	shift
done
