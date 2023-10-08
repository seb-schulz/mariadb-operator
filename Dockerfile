# FROM ghcr.io/flant/shell-operator:latest
FROM ghcr.io/flant/shell-operator:v1.3.2

ENV PATH="/venv/bin:$PATH"
ADD requirements.txt /requirements.txt

RUN apk add --no-cache mysql-client python3 && \
    python3 -m venv /venv && \
    /venv/bin/pip install -r /requirements.txt && \
    rm -f /requirements.txt

ADD hooks/* /hooks
