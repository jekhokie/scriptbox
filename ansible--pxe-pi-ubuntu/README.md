# Ansible PXE PI/Ubuntu

**NOTE**: This is a work in progress - the functionality within this project is not yet
fully functional.

Ansible project to install and configure components required for PXE-booting Raspberry Pi
instances. This Ansible project will configure the following components on the source
instance to enable other Raspberry Pi instances to connect and auto-provision according to
the way the PXE server/instances dictates it. The project is a good starting point for a
clean install of Raspbian (or other Operating Systems) for future testing/development:

- DHCP
- TFTP
- HTTP
- DNS

The project works with an Ubuntu 16.04 instance but is intended to be adapted to work on
a Raspbian system as well.

## Prerequisites

Install ansible on the source host (assumes install on Mac OSX using Homebrew):

```bash
$ brew install ansible
```

Next, set up the passwordless SSH keys for each of the source and target instance - it is
assumed you understand how to do this so this step will be skipped. The key name that is
assumed in the `hosts` file is `ansible-pxe`, but if you wish to change this name feel free
to update the `hosts` file appropriately.

Edit the `hosts.yml` file to ensure the `pxe-server` IP address matches your target Raspberry
Pi instance (or target Ubuntu 16.04 VM used for testing).

## Usage

Run the playbook against the target instance specified in the `hosts.yml` file:

```bash
$ ansible-playbook -i hosts site.yml
# you should see output corresponding to the actions being taken on the node
```

## Finish

Once the playbook completes, you should be able to boot any VM or Raspberry Pi instance on
the same network as the source PXE server and have it automatically allocate an IP address
and install the Raspbian operating system. From there, you can configure DNS (or drive DNS
first if you already know the MAC address of the target instance).
