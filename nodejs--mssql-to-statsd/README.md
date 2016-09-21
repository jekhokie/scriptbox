# MSSql to Statsd

This is a quick project set up to query a MSSql database, perform some calculations based on the results, and
send metrics along to a Statsd endpoint for storage of the metrics.

At this time, calculations are actually expected to be done on the MSSql side rather than this script side in
order to keep things very basic with generic handler capability.

## Database/Graphite/Statsd Prerequisites

This project assumes that the MSSql database and Graphite/Statsd are already installed and configured for use.

## Prerequisites

Install NodeJS and npm. Then, clone this repository and navigate to this example:

```bash
$ git clone https://<git_location>/scriptbox.git
$ cd scriptbox/nodejs--mssql-to-statsd
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

Specify the functions and corresponding metrics to send to statsd within the `perform-queries.js` script.
Note that this is done in this fashion due to the data type limitations of `dotenv` not supporting hash
structures, as well as the fact that with enhancements, it is likely that calculator functions are to be
written in the script for each query that is performed (thus making it even less reasonable to manage the
queries outside of the script scope):

```bash
$ vim perform-queries.js
# edit the section labeled "CONFIGURE QUERIES" via the instructions provided - note that all queries must
# result in a single row returned with a key of "COUNT" and a numerical value
```

## Usage

Now that the configurations are in place, run the script to interact with the MSSql database and send
information to the environment-specified Statsd service.

```bash
$ nodejs perform-queries.js
# you should see output corresponding to the request/response sequence
```
