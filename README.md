# k0s-on-vagrant-template

This template repository should help to bootstrap a new project on kubernetes faster.
It installs [k0s](https://k0sproject.io/) on (vagrant)[https://www.vagrantup.com/] and exports a kubeconfig file so that access to the kubernetes cluster from host machine is possible.

## Prerequisite

* vagrant
* vagrant-libvirt plugin
* vagrant-sshfs plugin

## How to setup the environment

1. Modify your Vagrantfile so that it fits to your need (e.x. cpu, memory)
2. Kickoff a virtual machine with `vagrant up`
3. Set environment variable for `kubectl` with `export KUBECONFIG=kubeconf.conf`


Enjoy!
