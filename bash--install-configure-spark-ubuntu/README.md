# Install and Configure Apache Spark

Bash script to install and configure an Apache Spark node on an Ubuntu 16.04-based system using the
standalone Spark (non-YARN, non-Mesos) manager.

This installation script will install Apache Spark version 2.0.1, including the corresponding required
Scala version, 2.11. You may wish to adjust these versions, but adjustments have not been tested and
may not work as expected.

Note that this script was developed for and tested on an Ubuntu 16.04 installation - it may work on
other versions of Ubuntu, but as always, YMMV.

## Prerequisites

This script simply requires an Ubuntu 16.04 instance (or set of instances) that can connect to the
public internet (for downloading required dependencies/packages). It can be configured to install
the master node as well as optional slave nodes, clustering as appropriate.

## Hardware

The following specifications are expected for this script to function and install a properly-optimized
Spark instance. Again, other specs may work, but YMMV.

* OS: Ubuntu 16.04
* Arch: 64-bit
* Disk: 50GB
* CPU: 2

## Usage

Run this script on any/all Ubuntu 16.04 nodes that you wish to configure as a Spark node. Note that you
*MUST* run the script as the root user as it requires root privileges to install and configure various
system packages and dependencies.

At least 1 master node is required - slave nodes are optional and can be configured via the environment
settings at the front of the script.

```bash
$ sudo vim install_configure_spark.sh
# edit the up-front variables to suit your environment

$ sudo ./install_configure_spark.sh
```

Once running the script, you should see various output commands corresponding to the installation and
configuration of the software/services.

## Moving Forward

Note that the above setup/script does not account for *ALL* important configurations related to running
a production Spark service. In addition, it focuses on using an IP address-based scheme for communication
and clustering, which is likely less desirable and hostnames should be used in favor of IP addresses.

## Credit

Some of the process defined in this script is taken from the instruction in the following posts:

* [Spark Standalone](https://spark.apache.org/docs/latest/spark-standalone.html)
