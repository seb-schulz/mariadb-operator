# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  ssh_pub_key = File.readlines("#{Dir.home}/.ssh/id_ed25519.pub").first.strip

  config.vm.box = "debian/testing64"

  config.vm.provider "libvirt" do |vb, override|
    vb.memory = 4*1024
    vb.cpus = 4
  end

  config.vm.synced_folder './', '/vagrant', type: 'sshfs'

  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "provisioning/playbook.yml"
  end



  config.vm.post_up_message = <<-MSG
Vanilla Debian box. See https://app.vagrantup.com/debian for help and bug reports
Execute `export KUBECONFIG=kubeconf.conf` to get access to the k8s cluster with `kubectl`
  MSG
end
