# Python Learnings

Collection of scripts and functionality to demonstrate core Python 3 concepts to brush up/stay current.
Each script in this directory demonstrates a discrete piece of functionality/concept within Python and
is self-documented to explain the details behind the functionality.

## Prerequisites

Install easy_install, pip3 and virtualenv. Then, clone this repository and navigate to this example:

```bash
$ git clone https://<git_location>/scriptbox.git
$ cd scriptbox/python--learnings/
```

Install the required environment and libraries, making sure to specify the use of Python 3:

```bash
$ virtualenv -p /usr/local/bin/python3 --no-site-packages --distribute .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

You can validate that you have Python 3 in your environment by running the `python --version` command, which
should return that it is using a version of Python 3.

## Usage

There are various example scripts each named with core functionality. Simply run the script you wish to learn
functionality about and it will output test results for the functionality:

```bash
$ python -m unittest generators_iterators.py
# should output test results
```

You can inspect the script for comments to learn how the functionality is developed/structured and read the
tests to understand any sequencing.
