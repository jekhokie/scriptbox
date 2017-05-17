# Jira Query

This script performs a JQL query against a user-specified Jira instance.

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
# lock the file down for sensitive information
```

## Executing

Run the script:

```bash
$ bundle exec ruby jira-query.rb
```
