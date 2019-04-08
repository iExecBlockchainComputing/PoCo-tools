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

INPUT="result.zip"
PUB_KEY=".tee-secrets/beneficiary/0x4d65930f53da6C277F1769170Df69d772a492008_key.pub"

if [ $# -ge 1 ]; then INPUT=$1; fi
if [ $# -ge 2 ]; then PUB_KEY=$2; fi

if [ ! -f "$INPUT" ]; then echo "missing input file '$INPUT'"; exit 255; fi
if [ ! -f "$PUB_KEY" ]; then echo "missing key file '$PUB_KEY'"; exit 255; fi


ROOT_FOLDER="iexec_out"
ENC_RESULT_FILE="result.zip.aes"
ENC_KEY_FILE="encrypted_key"
TMP_KEY_FILE=".iexec-tee-temporary-key"
IV_FILE=".iexec-tee-iv-key"

KEY_LENGTH=16 # 16 bytes = 128bits (for 2048 bits RSA keys)
IV_LENGTH=16

case ${KEY_LENGTH} in
	16) AES_ALG="-aes-128-cbc";;
	32) AES_ALG="-aes-256-cbc";;
	*) exit 1
esac

### MAKE ROOT FOLDER IF NOT EXIST
mkdir -p ${ROOT_FOLDER}

### GENERATE AES KEY
KEY=$(openssl rand ${KEY_LENGTH} | tee ${TMP_KEY_FILE} | od -An -tx1 | tr -d ' \n')
# echo "KEY:" ${KEY}

### GENERATE IV
IV=$(openssl rand ${IV_LENGTH} | tee ${IV_FILE} | od -An -tx1 | tr -d ' \n')
# echo "IV:" ${IV}

### ENCRYPT RESULT AND AES KEY
mv ${IV_FILE} ${ROOT_FOLDER}/${ENC_RESULT_FILE}
openssl enc ${AES_ALG} -K ${KEY} -iv ${IV} -in ${INPUT} >> ${ROOT_FOLDER}/${ENC_RESULT_FILE}
openssl rsautl -encrypt -oaep -inkey ${PUB_KEY} -pubin -in ${TMP_KEY_FILE} >> ${ROOT_FOLDER}/${ENC_KEY_FILE}

### ZIP
zip -r ${ROOT_FOLDER} ${ROOT_FOLDER}/${ENC_RESULT_FILE} ${ROOT_FOLDER}/${ENC_KEY_FILE}

### REMOVE TEMPORARY FILES
rm ${ROOT_FOLDER}/${ENC_RESULT_FILE} ${ROOT_FOLDER}/${ENC_KEY_FILE}

### SHRED KEY
shred -u ${TMP_KEY_FILE}
KEY=""

echo "Result succesfully encrypted to '${ROOT_FOLDER}.zip'"
