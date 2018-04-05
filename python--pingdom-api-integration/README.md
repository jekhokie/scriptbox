# Pingdom API Integration

This is a quick project set up to test the integration with the Pingdom (http://pingdom.com/) API endpoint.

## Prerequisites

Install easy_install, pip and virtualenv. Then, clone this repository and navigate to this example:

```bash
$ git clone https://<git_location>/scriptbox.git
$ cd scriptbox/python--pingdom-api-integration
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

Now that the configurations are in place, run the script to interact with the Pingdom service.

```bash
$ python check_demo.py
# you should see output corresponding to the request/response sequence
```
