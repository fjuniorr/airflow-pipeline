# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "bento/ubuntu-22.04"

  config.vm.network "private_network", ip: "192.168.33.50"
  config.ssh.forward_agent = true

  config.vm.synced_folder "dags/", "/home/vagrant/airflow/dags/"

end
