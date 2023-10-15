#!/usr/bin/bash

set -xeu

direction=$1
target_host=${2:-mariadb-operator}

case "${direction}" in
    push)
        rsync_args=--delete
        src=./
        dest=${target_host}:/workspace/mariadb-operator
        ;;
    pull)
        src=${target_host}:/workspace/mariadb-operator/
        dest=./
        ;;
    *)
        exit 1
        ;;
esac

pushd $(realpath $(dirname $0)/..)
trap popd EXIT

rsync -avz --exclude=.git --exclude=.vagrant --progress ${rsync_args:-} ${src} ${dest}
