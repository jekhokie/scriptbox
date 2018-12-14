# Ansible AWX

Ansible project to install the Ansible AWX software, an open-source version of the
Ansible Tower UI for controlling Ansible playbooks.

This project assumes a node running CentOS 7 and having 2x CPU, 4GB RAM. It also
assumes that you are running and controlling the VM using Vagrant.

## Prerequisites

Install ansible on the source host (assumes install on Mac OSX using Homebrew):

```bash
$ brew install ansible
```

Next, set up the passwordless SSH keys for each of the source instance and target VM - it is
assumed you understand how to do this so this step will be skipped. The key name that is
assumed in the `hosts` file is `ansible-awx`, but if you wish to change this name feel free
to update the `hosts` file appropriately.

Edit the `hosts.yml` file to ensure the node1 IP address match your target VM instance.

## Usage

Run the playbook against the target instance specified in the `hosts.yml` file:

```bash
$ ansible-playbook -i hosts site.yml
# you should see output corresponding to the actions being taken on the node
```

## Check AWX

Once the playbook completes, you should be able to log into the AWX  interface at the
following URL:

[http://10.11.13.15/](http://10.11.13.15/)

The default login username is `admin` and password is `password`.
