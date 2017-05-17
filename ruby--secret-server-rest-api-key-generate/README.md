# Secret Server REST API Key Generate

This script accepts input arguments for a user ID and corresponding REST service and
generates an OAuth 1.0a secret in [Thycotic Secret Server](https://thycotic.com/products/secret-server/),
which contains a key name and corresponding password for the user to use.

## Prerequisites

Install RVM according to the installation instructions on the website:

- https://rvm.io/

Install bundler:

```bash
$ gem install bundler
```

Install the required gems:

```bash
$ bundle install
```

## Configuration

Copy the sample configuration file and configure with your environment settings:

```bash
$ cp config/settings.yml.sample config/settings.yml
# edit settings.yml to reflect your actual configuration settings

$ chmod 600 config/settings.yml
# secure the sensitive file
```

## Executing

Run the script:

```bash
$ bundle exec ruby ./create_api_key_secret.rb -u someuser -s rest-service
```
