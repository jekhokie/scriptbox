# Ansible Jenkins 2 Instance

Another small Ansible project to install and configure Jenkins in a remote VM. Yes,
again, this is something that there is already an Ansible module for, but in the spirit
of continuing to practice Ansible and learn how things get installed, I am writing this
Ansible code.

This project assumes 1 node, and will install Jenkins 2. The node should be running an
Ubuntu 16.04 operating system with at least 2x CPU and 4GB RAM.

## Prerequisites

Install ansible (assumes install on Mac OSX using Homebrew):

```bash
$ brew install ansible
```

Next, set up the passwordless SSH keys for each of the source instance and target VM - it is
assumed you understand how to do this so this step will be skipped. The key name that is
assumed in the `hosts` file is `ansible-jenkins2`, but if you wish to change this name feel free
to update the `hosts` file appropriately.

Edit the `hosts.yml` file to ensure the `jenkins` IP address matches your target VM instances.

## Usage

Run the playbook against the target instance specified in the `hosts.yml` file:

```bash
$ ansible-playbook -i hosts site.yml
# you should see output corresponding to the actions being taken to install Jenkins
```

## Check Jenkins

Once the playbook completes, you should be able to log into the Jeknins interface via the
following URL:

[http://10.11.13.15:8080/](http://10.11.13.15:8080/)

Follow the instructions in the UI to proceed with the rest of the setup and usage of Jenkins.
For starters, you'll likely need the activation code which can be found via running the following
command on the Jenkins host VM:

```bash
$ cat /var/lib/jenkins/secrets/initialAdminPassword
```

From here, you should be off to the races!
