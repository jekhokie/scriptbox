# Vagrant Kubernetes/Istio Cluster

A mixed technology project that configures a Kubernetes + Istio (plus several other exploratory plugins)
cluster on a host machine using Vagrant + VirtualBox.

Hardware:

- MacBook Pro with 32GB RAM

Open source technologies used:

- Vagrant
- VirtualBox
- Ansible
- Docker
- Kubernetes
- Istio

Kubernetes/other plugins used:

- Calico (networking)

## Some Notes

This repository has a lot more in it than just creating a Vagrant k8s cluster. There are many sub-directories
not mentioned in this README file. Specifically, the contents of this repo also support the blog
[https://jekhokie.github.io](https://jekhokie.github.io) and you can see much of its contents used in several
Kubernetes-focused tutorials in that blog.

## Prerequisites

This repo assumes that you already have a functioning Vagrant + VirtualBox setup. In addition, you need
to install the Vagrant `vbguest` plugin, which enables handling installation and configuration of VirtualBox
Guest additions for local storage sharing automatically on boot of the VM instance:

```bash
$ vagrant plugin install vagrant-vbguest
```

Next, you'll want to use a box that already has guest additions installed if at all possible. The above sets
the environment up in case you discover/use boxes that don't already have guest additions installed, but ideally
you'll want these pre-installed as the provisioning process takes a few minutes (longer than reasonable). If
you decide not to run the following commands, you'll want to edit the `Vagrantfile` to specify the correct box
to use as the existing `Vagrantfile` in this repo declares the box to be used in this tutorial:

```bash
$ vagrant box add centos7-with-guest https://github.com/vezzoni/vagrant-vboxes/releases/download/0.0.1/centos-7-x86_64.box
```

Additionally, each time you run the `vagrant up master` command, temporary artifacts will be created in the
Vagrant shared directory. Make sure if you are tearing down/re-building a cluster, you clean the directory
first (all contents, including tokens, etc.) as this directory contains artifacts that, if not removed, will
not be overwritten on your local workstation and would result in worker nodes being prevented from joining
the cluster (having the wrong token/token hash). You can use the following script to clean the environment:

```bash
$ clean.sh
```

## Usage

To create a cluster, first start with the master/control node from within the root directory of this repository:

```bash
$ vagrant up master
```

The above process will take some time as it works through the provisioning process. Once complete, there will
be several files stored as part of the shared directory with the guest VM, one of which is the `admin.conf` which
enables communication with the cluster (note: this is an admin-level permission set, so be careful with storage
of this file):

```bash
# from your local/host workstation
$ kubectl --kubeconfig shared/kubernetes/admin.conf get nodes

# master node should display "Ready" for STATUS, then you can proceed
# note that this will likely take a few minutes while it bootstraps
```

Next, inspect the pods running on the master:

```bash
# from your local/host workstation
$ kubectl --kubeconfig shared/kubernetes/admin.conf get pods -n kube-system

# you should see the following pods "Running" at a minimum
#    calico
#    coredns
#    etcd
#    kube-apiserver
#    kube-controller-manager
#    kube-proxy
#    kube-scheduler
```

Once your master node is up and running, you can provision your worker nodes. This repository supports 2
worker nodes (maximum that can reasonably be supported on a device with 32GB RAM and still leave room for
the OS and other workstation processes):

```bash
$ vagrant up
# wait for the node1 and node2 provisioning to complete

# check the cluster status
$ kubectl --kubeconfig shared/kubernetes/admin.conf get nodes
# all nodes should show "Ready" in due time, indicating the cluster
# is now formed/functional and ready for workloads
```

## Todo

There are a few things in here that could use improvement - this is just a way to capture those as they
are discovered and may/may never be resolved:

- Convert to overlay2 (requires d_type=true support for XFS filesystem - figure out how to launch a Vagrant
VM with d_type=true enabled for the main XFS filesystem).
- Ansible - right now everything runs through single localhost with all roles defined and master-only and
worker-only tasks filtered with 'when' clauses. Remote administration may be better eventually to avoid
needing to provide `when` conditions for determining state.

## Sources

Some sources used for putting this together:

- https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/
- https://kubernetes.io/docs/setup/production-environment/container-runtimes/
- https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init/#automating-kubeadm
