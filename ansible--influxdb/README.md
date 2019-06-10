# Ansible InfluxDB Installation

Small Ansible project to install and configure InfluxDB on a RedHat/CentOS instance.

This project assumes 1 node, and will install InfluxDB. The node should be running an
RedHat/CentOS 7.x operating system with at least 2x CPU and 4GB RAM.

## Prerequisites

Install ansible (assumes install on Mac OSX using Homebrew):

```bash
$ brew install ansible
```

Next, set up the passwordless SSH keys for each of the source instance and target VM - it is
assumed you understand how to do this so this step will be skipped. The key name that is
assumed in the `hosts` file is `ansible-influxdb`, but if you wish to change this name feel free
to update the `hosts` file appropriately.

Edit the `hosts.yml` file to ensure the `influxdb` IP address matches your target VM instances.

## Usage

Run the playbook against the target instance specified in the `hosts.yml` file:

```bash
$ ansible-playbook -i hosts site.yml
# you should see output corresponding to the actions being taken to install InfluxDB
```

*NOTE*: The `common` role also installs and configures `firewalld` to ensure that only SSH and port 8086
access are allowed (TCP) to the VM being configured.

## Check InfluxDB

Once the playbook completes, you should be able to open a web browser and navigate to the `/debug/vars`
path for the InfluxDB instance to see that InfluxDB is running and various settings/parameters available:

[http://10.11.13.50:8086/debug/vars](http://10.11.13.50:8086/debug/vars)

From here, you should be off to the races!
