# README

```
ssh vagrant@127.0.0.1 -p 2222 -i .vagrant/machines/default/virtualbox/private_key
ansible vm -m ping
ansible-playbook airflow.yml
```

Running commands inside the vm

```
ansible vm -m command -a uptime
ansible vm -a "uptime" # command module is default
ansible vm -a "tail /var/log/dmesg"
ansible vm -b -a "tail /var/log/syslog" # become sudo
```


