# Install and Configure RabbitMQ

Bash script to install and configure a RabbitMQ cluster instance on an Ubuntu 14.04-based system.

Note that this script was developed for and tested on an Ubuntu 16.04 installation - it may work on
other versions of Ubuntu, but as always, YMMV.

## Prerequisites

This script simply requires an Ubuntu 16.04 instance (or set of instances) that can connect to the
public internet (for downloading required dependencies/packages).

The script will install a RabbitMQ service version 3.6.5-1 with corresponding Erlang dependency
version 1.18.2. These versions are pinned in the script in order to reduce complexities related to
multiple version accommodations.

## Hardware

The following specifications are expected for this script to function and install a properly-optimized
RabbitMQ cluster. Note that changing the specs below will most likely require you to update the script for
various parameters that are defined at the beginning of the script (i.e. memory settings, disk space, etc.).

* OS: Ubuntu 16.04
* Arch: 64-bit
* Disk: 50GB
* CPU: 2

## Usage

Run this script on any/all Ubuntu 16.04 nodes that you wish to cluster as a RabbitMQ cluster. Note that
you *MUST* run the script as the root user as it requires root privileges to install and configure various
system packages and dependencies. Prior to running, ensure that the up-front configuration variables are
set to match your environment - see the comments in the script for an explanation of each configuration
setting.

```bash
$ sudo vim install_configure_rabbitmq.sh
# configure the up-front environment variables for your environment

$ sudo ./install_configure_rabbitmq.sh
```

Once running the script, you should see various output commands corresponding to the installation and
configuration of the software/services. Following the installation, you should have a node that is either
a standalone configuration or clustered, and a management interface that can be accessed to view the
metrics related to the RabbitMQ service.

## Moving Forward

Note that the above setup/script does not account for *ALL* important configurations related to running
a production RabbitMQ cluster. For instance, there is no SSL support in communication between nodes in
the above configuration, which may be helpful/required in your setup depending on the type of information
you are seeking to transact through the system, the Erlang cookie is not locked down/secure, etc.
