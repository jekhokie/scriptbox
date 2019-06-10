# Ansible Grafana Installation

Small Ansible project to install and configure Grafana on a RedHat/CentOS instance.

This project assumes 1 node, and will install Grafana. The node should be running an
RedHat/CentOS 7.x operating system with at least 2x CPU and 4GB RAM.

**WARNING**: This is NOT a production-ready Grafana install. This setup does not include various
minimum requirements for a production-grade install such as LDAP-integrated user authentication and
authorization, valid SSL enablement, etc. This is intended to be a starting point for a production-
grade instance.

## Prerequisites

Install ansible (assumes install on Mac OSX using Homebrew):

```bash
$ brew install ansible
```

Next, set up the passwordless SSH keys for each of the source instance and target VM - it is
assumed you understand how to do this so this step will be skipped. The key name that is
assumed in the `hosts` file is `ansible-grafana`, but if you wish to change this name feel free
to update the `hosts` file appropriately.

Edit the `hosts.yml` file to ensure the `grafana` IP address matches your target VM instances.

## Usage

Run the playbook against the target instance specified in the `hosts.yml` file:

```bash
$ ansible-playbook -i hosts site.yml
# you should see output corresponding to the actions being taken to install Grafana
```

*NOTE*: The `common` role also installs and configures `firewalld` to ensure that only SSH and port 3000
access are allowed (TCP) to the VM being configured.

## Check Grafana

Once the playbook completes, you should be able to open a web browser and navigate to the Grafana base
path to see that Grafana is installed and running:

[http://10.11.13.50:3000/](http://10.11.13.50:3000/)

Log in using the default username and password (`admin` / `admin`). From here, you should be off to
the races!
