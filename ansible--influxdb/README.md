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

## Create Users for Authentication

InfluxDB authentication only executes (even though enabled by default with this Ansible role) if there is
an 'admin' user. Let's create an admin user to start:

{% highlight bash %}
$ influx -execute "CREATE USER admin WITH PASSWORD 'supersecretpassword' WITH ALL PRIVILEGES"
{% endhighlight %}

Now that an admin user exists, let's create a database and separate read and write users:

{% highlight bash %}
# create 'test' database
$ influx -execute "CREATE DATABASE test"

# create read-only user and grant privileges to 'test' DB
$ influx -execute "CREATE USER ro_user WITH PASSWORD 'secretropassword'"
$ influx -execute "GRANT READ ON test TO ro_user"

# create read/write user and grant privileges to 'test' DB
$ influx -execute "CREATE USER rw_user WITH PASSWORD 'secretrwpassword'"
$ influx -execute "GRANT WRITE ON test TO rw_user"
{% endhighlight %}

At this point, you should be able to write data to the database using the 'rw_user' user, and only read
data from the database using the 'ro_user' user:

{% highlight bash %}
# attempt to insert and read data with read/write user - should succeed
$ influx -execute "INSERT cpu,host=testhost value=0.2" -database test -username rw_user -password secretrwpassword
$ influx -execute "SELECT * FROM cpu" -database test -username rw_user -password secretrwpassword

# attempt to insert and read data with read-only user - should fail on write/succeed on read
$ influx -execute "INSERT cpu,host=testhost value=0.1" -database test -username ro_user -password secretropassword
$ influx -execute "SELECT * FROM cpu" -database test -username ro_user -password secretropassword
{% endhighlight %}
