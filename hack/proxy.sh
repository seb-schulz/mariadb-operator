set -xeu

kubectl --kubeconfig=$(realpath $(dirname $0))/../kubeconf.conf port-forward deployments/mariadb 22222:22 > /dev/null &
trap "kill $!" EXIT

while ! nc -z localhost 22222; do
    sleep 0.2
done

nc localhost 22222
