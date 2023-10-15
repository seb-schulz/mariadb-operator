#! /usr/bin/bash

set -xeu

if [ ! -d /vagrant ];  then
    vagrant ssh -- /vagrant/hack/build.sh
    exit 0
fi

pushd $(realpath $(dirname $0)/..)
trap popd EXIT

authorized_keys=$(cat ${HOME}/.ssh/authorized_keys | base64 -w0)

buildah bud --squash -f hack/Dockerfile -t ghcr.io/seb-schulz/mariadb-operator:dev --build-arg "SSH_AUTHORIZED_KEYS=${authorized_keys}"
