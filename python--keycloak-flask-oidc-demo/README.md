# Keycloak Python Flask OpenID Connect (OIDC) Tutorial

Project to create a Python Flask application that integrates with the open source Identity and Access
Management (IAM) utility Keycloak using OpenID Connect (OIDC) and OAuth 2.0.

## Prerequisites

There are a few prerequisites required in order for this application to function, as noted below.

### Keycloak

This application assumes you already have an installed and reachable Keycloak application running
somewhere that the Flask application can access it.

### Python Files and Libraries

Install easy_install, pip and virtualenv. Then, clone this repository and navigate to this example:

```bash
$ git clone https://<git_location>/scriptbox.git
$ cd scriptbox/python--keycloak-flask-oidc-demo/
```

Install the required environment and libraries.

**NOTE**: Make sure you use Python 3.

```bash
$ virtualenv --python /usr/local/bin/python3 --no-site-packages --distribute .env
$ source .env/bin/activate
$ python --version
# should return version 3
$ pip install -r requirements.txt
```

### Configuration

There are a couple of configuration files that need to be set in order for the application to function.
Create copies of the sample files and enter the respective details for your environment:

```bash
$ cp config/settings.yml.sample config/settings.yml
$ cp config/client_secrets.json.sample config/client_secrets.json
$ chmod 640 config/settings.yml config/client_secrets.json
```

Edit the newly-created files (from the template) with your respective environment details.

## Usage

To start the Flask application, simply run the `run.py` script:

```bash
$ python run.py
```

You can now open a browser and navigate to http://<SERVER_IP>:8000/ to see the landing page and interact
with the Flask application.
