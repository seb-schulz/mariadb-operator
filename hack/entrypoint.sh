#!/bin/sh
mkdir -p /run/sshd
ssh-keygen -A
exec /usr/sbin/sshd -D -e "$@"
