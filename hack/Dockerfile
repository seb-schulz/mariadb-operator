# FROM ghcr.io/seb-schulz/mariadb-operator:latest as shell-operator
FROM ghcr.io/flant/shell-operator:v1.3.2 as shell-operator

FROM docker.io/python:3.11

ARG SSH_AUTHORIZED_KEYS

ENV PATH="/venv/bin:$PATH"
ADD requirements.txt /requirements.txt

RUN set -xeu && apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -qq install mariadb-client-core curl bind9-dnsutils openssh-server rsync jq && \
    mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    echo "$SSH_AUTHORIZED_KEYS" | base64 -d > /root/.ssh/authorized_keys && \
    mkdir -p /workspace/mariadb-operator && \
    rm -rf /var/lib/apt/lists/* && \
    python3 -m venv /venv && \
    /venv/bin/python3 -m pip install --upgrade pip && \
    /venv/bin/pip install -r /requirements.txt && \
    rm -f /requirements.txt && \
    curl -LO https://dl.k8s.io/release/$(curl -LS https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl

COPY --from=shell-operator /shell-operator /shell-operator
COPY --from=shell-operator /frameworks /
COPY --from=shell-operator /shell_lib.sh /

ENV SHELL_OPERATOR_HOOKS_DIR /workspace/mariadb-operator/hooks
ENV LOG_TYPE json

WORKDIR /

EXPOSE 22
COPY hack/entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]
CMD []
