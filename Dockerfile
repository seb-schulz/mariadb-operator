# FROM ghcr.io/flant/shell-operator:latest
FROM ghcr.io/flant/shell-operator:v1.3.2

RUN apk add --no-cache mysql-client

ADD hooks/* /hooks
