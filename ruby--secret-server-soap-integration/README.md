# Secret Server SOAP Integration

This script performs several different functions to demonstrate SOAP integration with a
[Thycotic Secret Server](https://thycotic.com/products/secret-server/) instance.

## Prerequisites

Install RVM according to the installation instructions on the website:

- https://rvm.io/

Install bundler:

```bash
$ gem install bundler
```

Set the C-compiler location:

```bash
$ export CC=/usr/bin/gcc
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
# lock down the sensitive file
```

## Executing

Run the script:

```bash
$ bundle exec ruby ./integrate_with_secret_server.rb
```
