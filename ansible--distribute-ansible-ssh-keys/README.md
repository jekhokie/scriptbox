# Distribute Ansible SSH Keys

Often times if the `ansible` user SSH keys are not baked into whatever image or template is being used
for creating VMs for an environment, it becomes necessary to use a local operator account that has
sudo privileges available to first distribute the SSH keys prior to running any playbooks. This playbook
takes the public SSH key of the `ansible` user, and as the local operator account, installs the public key
into the `authorized_keys` file to allow for SSH access by the ansible user.  Additionally, the playbook
configures the `ansible` user for password-less sudo privileges.

## Configure Target Hosts

This test playbook assumes that the user will update the variable list first of the target machines as
well as where the public key of the ansible user is located. Copy the sample `hosts` file and enter details
for 1:n hosts you wish to target for this playbook:

```bash
$ cp hosts.sample hosts
$ vim hosts
# edit this file to include the hostnames and IP addresses (if the hostnames are
# not resolvable) of the hosts you wish to target for SSH key distribution
```

## Generate SSH Key for User

This playbook installs a user's public SSH key on a target machine as well as updates the authorized_keys
file. We'll first generate an SSH key for the target `ansible` user to use:

```bash
$ ssh-keygen -t rsa -b 2048 -f roles/common/files/ansible
# ensure no password is present when prompted (press Enter without specifying a password)
```

The above command will create 2 files, one being the private key and the other being the public key
for the `ansible` user. Make sure you PROTECT the private key as this will drive access to all of the
specified target systems in your `hosts` file.

## Run the Playbook

Run the playbook command and specify your user account (or a user account that you wish to SSH into
the VMs with). Note that the account being used to distribute the keys in this particular case must
not only have SSH access but sudo privileges on the target instances.

The playbook command below will prompt you for a password for login/sudo.

*NOTE*: The `-c paramiko` part of this command is required in order to run the remote SSH command
through ansible - failure to specify this switch/option is likely to generate an error similar to
`to use the 'ssh' connection type with passwords, you must install the sshpass program`.

```bash
$ ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i hosts site.yml --user my_user --ask-pass -c paramiko
# enter the login credentials for your own user when requested
```

Following the script execution, you should have the public ansible SSH key generated previously
installed on the remote systems.

## Test Access

We can now test access to the remote systems, proving the playbook worked as expected. Using the
private key previously generated, log into the remote system as the `ansible` user and sudo to
root, which should work without a password:

```bash
$ ssh -i roles/common/files/ansible ansible@<REMOTE_HOSTNAME_OR_IP>
$ sudo su -
```

If the above commands work as expected (SSH with key and sudo without password) then you now
have a fully functional `ansible` account on the target machine!
