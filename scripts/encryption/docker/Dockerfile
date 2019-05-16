FROM alpine:3.9.4

RUN apk --no-cache add bash
RUN apk --no-cache add openssl

COPY datasetEncrypt.sh /datasetEncrypt.sh
RUN chmod +x /datasetEncrypt.sh
ENTRYPOINT ["/datasetEncrypt.sh"]
