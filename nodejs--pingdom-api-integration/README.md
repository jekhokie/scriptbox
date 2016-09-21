# Pingdom API Integration

This is a quick project set up to test the integration with the Pingdom (http://pingdom.com/) API endpoint.

## Prerequisites

Install NodeJS and npm. Then, clone this repository and navigate to this example:

```bash
$ git clone https://<git_location>/scriptbox.git
$ cd scriptbox/nodejs--pingdom-api-integration
```

Install the required environment and libraries:

```bash
$ npm install
```

Create a configuration file from the sample and specify the values for your specific environment.

```bash
$ cp config/.env.sample config/.env
# edit the config/.env file for your environment
$ chmod 600 config/.env
# lock down the file as it contains sensitive information
```

## Usage

Now that the configurations are in place, run the script to interact with the Pingdom service.

```bash
$ nodejs make-request.js
# you should see output corresponding to the request/response sequence
```
