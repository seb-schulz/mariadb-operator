# FROM ghcr.io/seb-schulz/mariadb-operator:latest as shell-operator
FROM ghcr.io/flant/shell-operator:v1.3.2 as shell-operator

FROM docker.io/python:3.11

ARG SSH_AUTHORIZED_KEYS
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV PATH="/venv/bin:$PATH"
ADD requirements.txt /requirements.txt

RUN set -xeu && \
    groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -qq install mariadb-client-core curl bind9-dnsutils openssh-server rsync jq sudo && \
    mkdir -p /home/$USERNAME/.ssh && \
    chmod 0700 /home/$USERNAME/.ssh && \
    echo "$SSH_AUTHORIZED_KEYS" | base64 -d > /home/$USERNAME/.ssh/authorized_keys && \
    chmod 600 /home/$USERNAME/.ssh/authorized_keys && \
    chown -R $USER_UID:$USER_GID /home/$USERNAME/.ssh && \
    mkdir -p /workspace/mariadb-operator && \
    rm -rf /var/lib/apt/lists/* && \
    python3 -m venv /venv && \
    /venv/bin/python3 -m pip install --upgrade pip && \
    /venv/bin/pip install -r /requirements.txt && \
    rm -f /requirements.txt && \
    curl -LO https://dl.k8s.io/release/$(curl -LS https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl && \
    echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

COPY --from=shell-operator /shell-operator /shell-operator
COPY --from=shell-operator /frameworks /
COPY --from=shell-operator /shell_lib.sh /

COPY hack/entrypoint.sh /

ENV SHELL_OPERATOR_HOOKS_DIR /workspace/mariadb-operator/hooks
ENV LOG_TYPE json

WORKDIR /workspace/mariadb-operator
EXPOSE 22

ENTRYPOINT ["/entrypoint.sh"]
CMD []
