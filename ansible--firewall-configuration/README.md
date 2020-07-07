# Firewall Configuration

Configuring IPTables for RHEL-based Operating Systems in ansible can be cumbersome if you require ordering
of your firewall rules. There is an improved `iptables_raw` module available, but to work around the issue
of the built-in `iptables` module that does not allow for ordering, you can also utilize a file (or template)
to drive the IPTables configuration file and have changes to the file drive a restart/reload of the firewall
rules. This project demonstrates the latter (static-defined IPTables configuration file driving restarts and
reloads of the `iptables` service in RHEL-based systems).

*NOTE*: This project assumes that you already have a target system configured for interaction using a service
account named `ansible`.

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

## Run the Playbook

Run the playbook against the target instances to configure the firewall:

```bash
$ ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i hosts site.yml
```

Following the script execution, IPTables on the target instance should be configured.

## Test Firewall

Once the playbook completes execution, you can test that the firewall is configured as expected. The
file with the rules that is used for the firewall is in the `roles/common/files/` directory named
`iptables`, and is configured to ensure that only port 22 is open to remote instances. We can use the
`nmap` tool to test that port 22 is open and prove that other ports are in fact filtered by the firewall.
From the VM that this script is installed on/run from:

```bash
$ nmap -p 22 <TARGET_HOSTNAME_OR_IP>
# should output something similar to the following, indicating port 22 is open:
#   ...
#   PORT   STATE SERVICE
#   22/tcp open  ssh
#   ...

$ nmap -p 23 <TARGET_HOSTNAME_OR_IP>
# should output something similar to the following, indicating port 23 is filtered by the firewall:
#   ...
#   PORT   STATE    SERVICE
#   23/tcp filtered telnet
#   ...

# try nmap with a few more ports (non-port 22) to ensure they are filtered,
# or re-run without specifying a port to do a full port scan and prove that only
# port 22 (SSH) is open via the firewall
```

If the above commands produce output as detailed, your firewall rules have been successfully deployed!
