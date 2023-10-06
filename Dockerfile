FROM ghcr.io/flant/shell-operator:latest

RUN apk add --no-cache mysql-client

ADD hooks/* /hooks
