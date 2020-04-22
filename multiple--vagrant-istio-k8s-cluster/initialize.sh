#!/bin/bash

ANSIBLE_DIR=/vagrant_data/ansible

echo "installing epel-release for latest ansible"
yum -y install epel-release

echo "installing ansible"
yum -y install ansible

echo "bootstrapping host using ansible"
ansible-playbook -i $ANSIBLE_DIR/hosts $ANSIBLE_DIR/ready-host.yml
