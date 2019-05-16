FROM alpine:3.9.4

RUN apk --no-cache add bash
RUN apk --no-cache add openssl

RUN adduser -D -u 1000 encryptor
WORKDIR /home/encryptor
COPY datasetEncrypt.sh .
RUN chmod +x datasetEncrypt.sh

USER encryptor

ENTRYPOINT ["./datasetEncrypt.sh"]
