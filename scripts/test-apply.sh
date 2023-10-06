#!/bin/bash

set -xeu

image=$1
tag=$2

sudo k0s ctr --namespace=k8s.io i ls -q | grep ${image} | xargs sudo k0s ctr --namespace=k8s.io i rm

buildah push ${image}:${tag} oci-archive:/tmp/image.tar
sudo k0s ctr --namespace=k8s.io image import --digests --base-name ${image} /tmp/image.tar

k8s_image=$(sudo k0s ctr --namespace=k8s.io i ls -q | grep ${image})
rm /tmp/image.tar
