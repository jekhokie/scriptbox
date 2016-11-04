# Install and Configure Sensu

Bash script to install and configure a Sensu Server instance on an Ubuntu 16.04-based system.

Note that this script was developed for and tested on an Ubuntu 16.04 installation - it may work on
other versions of Ubuntu, but as always, YMMV.

## Prerequisites

This script simply requires an Ubuntu 16.04 instance (or set of instances) that can connect to the
public internet (for downloading required dependencies/packages). In addition, it is assumed that the
data store (Redis) and transport mechanism (RabbitMQ) specified are already installed, configured,
and reachable from the Sensu server node.

## Hardware

The following specifications are expected for this script to function and install a properly-optimized
Sensu instance. Again, other specs may work, but YMMV.

* OS: Ubuntu 16.04
* Arch: 64-bit
* Disk: 50GB
* CPU: 2

## Usage

Run this script on any/all Ubuntu 16.04 nodes that you wish to configure as a Sensu server node. Note that
you *MUST* run the script as the root user as it requires root privileges to install and configure various
system packages and dependencies.

```bash
$ sudo ./install_configure_sensu.sh
```

Once running the script, you should see various output commands corresponding to the installation and
configuration of the software/services.

## Moving Forward

Note that the above setup/script does not account for *ALL* important configurations related to running
a production Sensu service.

## Credit

Some of the process defined in this script is taken from the instruction in the following posts:

* [Sensu Server Installation](https://sensuapp.org/docs/0.25/installation)
