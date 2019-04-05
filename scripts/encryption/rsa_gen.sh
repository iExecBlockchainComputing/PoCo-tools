#generate key pair
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -out key.pem       
openssl rsa -pubout -in key.pem -out key.pub

