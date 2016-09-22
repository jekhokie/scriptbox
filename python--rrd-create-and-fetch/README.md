# RRD Create and Fetch

Scripts to demonstrate creating and fetching values from a Round Robin Database (RRD) file.

## Python-RRDTool Documentation

Documentation for the python-rrdtool library can be found here:

* http://pythonhosted.org/rrdtool/

## Compiler/Binary Prerequisites

The scripts in this project require the rrdtool binary and other development libraries to be
installed and available to the system. To handle the prerequisites, perform the following:

```bash
$ sudo apt-get install gcc
$ export CC=/usr/bin/gcc
$ sudo apt-get install libcairo2-dev libpango1.0-dev libglib2.0-dev libxml2-dev librrd-dev
$ sudo apt-get install rrdtool
```

## Prerequisites

Install easy_install, pip, and virtualenv. Then, clone this repository and navigate to this example:

```bash
$ git clone https://<git_location>/scriptbox.git
$ cd scriptbox/python--rrd-create-and-fetch
```

Install the required environment and libraries:

```bash
$ virtualenv --no-site-packages --distribute .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

## Usage

There are two scripts within the project - one script deals with creating and populating an RRD file,
and the other deals with parsing an RRD file for the last X seconds worth of information.

### Create RRD

To run the script which will create an RRD file 'rrds/test.rrd' and continuously populate it with
random integer values every 1 second:

```bash
$ ./create_rrd.py
# should expect to see output such as:
#   ...
#   Adding value '271' at epoch '1474320628'
#   Adding value '308' at epoch '1474320629'
#   Adding value '224' at epoch '1474320630'
#   Adding value '629' at epoch '1474320631'
#   Adding value '878' at epoch '1474320632'
#   Adding value '940' at epoch '1474320633'
#   Adding value '917' at epoch '1474320634'
#   Adding value '415' at epoch '1474320635'
#   Adding value '151' at epoch '1474320636'
#   Adding value '721' at epoch '1474320637'
#   ...
```

It is best to run this script in parallel with the fetch script, which will then get the values
for the last X seconds and display them.

### Fetch RRD

To fetch RRD data for the last 10 seconds (specified using the `--last-seconds` or `-l` command line
switch) from the file `rrds/test.rrd`:

```bash
$ ./fetch-rrd.js --last-seconds 10
# you should see output corresponding to the last 10 seconds, such as the following:
#   Start Epoch: 1474320628
#   End Epoch: 1474320637
#   Step: 1
#   DS: test
#   Values for last '10' seconds:
#   271
#   308
#   224
#   629
#   878
#   940
#   917
#   415
#   151
#   721
```
