# Ansible ELK Stack

This is a small Ansible project to create an ELK stack on a couple of target hosts. This
corresponds to a tutorial on the `jekhokie.github.io` blog titled "ELK Stack Install".
Yes, it is possible to re-use the already-existing ELK roles, but this was an exercise on
teaching how to construct an ELK stack and therefore built from the ground-up.

This project assumes 2 nodes, and will install the Elasticsearch instance on each node
along with a Kibana instance on node1 and a Logstash instance on node2. Each node should
be running an Ubuntu 16.04 operating system with at least 2x CPU and 4GB RAM.

## Prerequisites

Install ansible (assumes install on Mac OSX using Homebrew):

```bash
$ brew install ansible
```

Next, set up the passwordless SSH keys for each of the source instance and target VMs - it is
assumed you understand how to do this so this step will be skipped. The key name that is
assumed in the `hosts` file is `ansible-elk`, but if you wish to change this name feel free
to update the `hosts` file appropriately.

Edit the `hosts.yml` file to ensure the node1 and node2 IP addresses match your target VM
instances.

## Usage

Run the playbook against the target instances specified in the `hosts.yml` file:

```bash
$ ansible-playbook -i hosts site.yml
# you should see output corresponding to the actions being taken on each of
# the nodes specified in the hosts.yml file
```

## Check Kibana

Once the playbook completes, you should be able to log into the Kibana interface at the
following URL:

[http://10.11.13.15:5601/](http://10.11.13.15:5601/)

Once you create your index pattern (something like "filebeat-*") you should be able to start
parsing the system and audit logs from both hosts.
