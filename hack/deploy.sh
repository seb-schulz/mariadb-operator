#! /usr/bin/bash

set -xeu

if [ ! -d /vagrant ];  then
    vagrant ssh -- /vagrant/hack/deploy.sh
    exit 0
fi

pushd $(realpath $(dirname $0)/..)
trap popd EXIT

image=ghcr.io/seb-schulz/mariadb-operator

sudo k0s ctr --namespace=k8s.io i ls -q | grep ${image} | xargs sudo k0s ctr --namespace=k8s.io i rm
buildah push ${image}:dev oci-archive:/tmp/image.tar
sudo k0s ctr --namespace=k8s.io image import --digests --base-name ${image} /tmp/image.tar

k8s_image=$(sudo k0s ctr --namespace=k8s.io i ls -q | grep ${image})
rm /tmp/image.tar

helm uninstall mariadb deploy/mariadb || true
sleep 2
helm upgrade -i mariadb deploy/mariadb --set operator.imageOverride=${k8s_image} --set operator.image.pullPolicy=Never
