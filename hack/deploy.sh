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

kubectl --kubeconfig=kubeconf.conf apply -f- <<-EOL
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: mariadb-testenv
  namespace: default
rules:
  - apiGroups: ["k8s.sebatec.eu"]
    resources: ["databases", "users"]
    verbs: ["create", "delete"]
EOL

kubectl --kubeconfig=kubeconf.conf apply -f- <<-EOL
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: mariadb-testenv
  namespace: default
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: mariadb-testenv
subjects:
- kind: ServiceAccount
  name: mariadb-operator
  namespace: default
EOL

kubectl --kubeconfig=kubeconf.conf patch deployment mariadb -p '{"spec":{"template":{"spec":{"containers":[{"name":"operator","volumeMounts":[{"mountPath":"/workspace/mariadb-operator","name":"src"}]}],"volumes":[{"name":"src","persistentVolumeClaim":{"claimName":"src"}}]}}}}'
