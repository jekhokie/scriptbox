# Install and Configure Apache Kafka (and ZooKeeper)

Bash script to install and configure an Apache Kafka node on an Ubuntu 16.04-based system, including
the ZooKeeper dependency associated with running a Kafka cluster.

Note that this script was developed for and tested on an Ubuntu 16.04 installation - it may work on
other versions of Ubuntu, but as always, YMMV.

This script is not yet set up to configure a cluster of Kafka/ZooKeeper nodes - if/when such a capability
becomes useful to the prototyping being done, it will be added.

## Prerequisites

This script simply requires an Ubuntu 16.04 instance (or set of instances) that can connect to the
public internet (for downloading required dependencies/packages).

## Hardware

The following specifications are expected for this script to function and install a properly-optimized
Kafka instance. Again, other specs may work, but YMMV.

* OS: Ubuntu 16.04
* Arch: 64-bit
* Disk: 50GB
* CPU: 2

## Usage

Run this script on any/all Ubuntu 16.04 nodes that you wish to configure as a Kafka node. Note that you
*MUST* run the script as the root user as it requires root privileges to install and configure various
system packages and dependencies.

```bash
$ sudo vim install_configure_kafka.sh
# edit the up-front variables to suit your environment

$ sudo ./install_configure_kafka.sh
```

Once running the script, you should see various output commands corresponding to the installation and
configuration of the software/services.

## Moving Forward

Note that the above setup/script does not account for *ALL* important configurations related to running
a production Kafka service.
