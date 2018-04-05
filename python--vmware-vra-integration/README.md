# VMware vRA Integration

This is intended to be a starting point for a Python integration with VMware's vRealize Automation
(vRA) suite APIs for the purposes of provisioning and managing VMs.

## Prerequisites

Install easy_install, pip and virtualenv. Then, clone this repository and navigate to this example:

```bash
$ git clone https://<git_location>/scriptbox.git
$ cd scriptbox/python--vmware-vra-integration
```

Install the required environment and libraries:

```bash
$ virtualenv --no-site-packages --distribute .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

Create a configuration file from the sample and specify the values for your specific environment.

```bash
$ cp config/settings.yml.sample config/settings.yml
# edit the config/settings.yml file for your environment
```

## Usage

Now that the configurations are in place, run the script to create a VM in the target vRA environment.

```bash
$ python provision_vra_vm.py
# you should see output corresponding to the request/response sequence
# and it should take approximately 5 minutes to provision the VM end to end
```

## Future and Shortcomings

This repository should be updated to include things like returning the ID of the created VM
for the purposes of destroying the VM at a later date, returning the IP address so the user
knows how to reach the VM, etc. Again, this is just a simple integration and starting point.
