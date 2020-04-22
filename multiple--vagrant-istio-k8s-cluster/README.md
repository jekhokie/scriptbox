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

## Prerequisites

This repo assumes that you already have a functioning Vagrant + VirtualBox setup. In addition, you need
to install the Vagrant `vbguest` plugin, which enables handling installation and configuration of VirtualBox
Guest additions for local storage sharing automatically on boot of the VM instance:

```bash
$ vagrant plugin install vagrant-vbguest
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
