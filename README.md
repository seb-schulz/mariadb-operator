# MariaDB operator

This operator is based on [shell-operator](https://github.com/flant/shell-operator).
Goal of this operator is easily setup databases and users by using declaritive yaml configuration files.

# How to install on kubernetes

* `helm install mariadb deploy/mariadb`

# How to contribute

The development environment installs [k0s](https://k0sproject.io/) on (vagrant)[https://www.vagrantup.com/] and exports a kubeconfig file so that access to the kubernetes cluster from host machine is possible.

Please check the `Makefile` for further details.

## Prerequisite

* vagrant
* vagrant-libvirt plugin
* vagrant-sshfs plugin

## How to setup the environment

1. Modify your Vagrantfile so that it fits to your need (e.x. cpu, memory)
2. Kickoff a virtual machine with `vagrant up`
3. Set environment variable for `kubectl` with `export KUBECONFIG=kubeconf.conf`

Either run vagrant `ssh -- make -C /vagrant build test-latest` to get a container without dev-tools running or follow the next section to access the dev container.

## Working within the dev container

* Build dev container by running `vagrant ssh -- make -C /vagrant build build-dev test-dev`.
* Access the the operator container with `kubectl exec -ti deployments/mariadb -- bash`
* Within the container, establish a tunnel with `/code tunnel --name mariadb &` and follow the introduction.
* Run operator with `/shell-operator 2>&1 | jq -r .msg`

## Helper commands to troubleshoot issues

* `kubectl exec -ti deployments/mariadb -- bash -c 'mysql -h 127.0.0.1 -u root --password=$MARIADB_ROOT_PASSWORD -e "SELECT Host, User, Password FROM mysql.user;"'`
* `kubectl exec -ti deployments/mariadb -- bash -c 'mysql -h 127.0.0.1 -u root --password=$MARIADB_ROOT_PASSWORD -e "SHOW DATABASES"'`

Enjoy!
