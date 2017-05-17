# Secret Server SOAP Integration

This script performs several different functions to demonstrate SOAP integration with a
[Thycotic Secret Server](https://thycotic.com/products/secret-server/) instance.

WARNING: This script will end up printing sensitive/secret information to the console. Please
be careful running this script and ensure that any history/buffer in your terminal session is wiped
after running if there was sensitive data pulled.

## Prerequisites

Install easy_install, pip and virtualenv. Then, clone this repository and navigate to this example:

```bash
$ git clone https://<git_location>/scriptbox.git
$ cd scriptbox/python--secret-server-soap-integration
```

Install the required environment and libraries:

```bash
$ virtualenv --no-site-packages --distribute .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

Create a configuration file from the sample and specify the values for your specific environment. Make sure
to *lock down* the file as this file will contain secret information.

```bash
$ cp config/settings.yml.sample config/settings.yml
# edit the config/settings.yml file for your environment
$ chmod 600 config/settings.yml
```

## Usage

Now that the configurations are in place, run the script to perform a request against the Secret Server
instance using the account credentials specified in the configuration file.

```bash
$ python get_secret_server_secret.py
# you should see a JSON object printed to the screen containing all information about the secret
```
