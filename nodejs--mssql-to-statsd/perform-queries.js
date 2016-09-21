/*
Purpose: Query a MSSql database with given queries, aggregate results and perform calculations
         desired, and forward calculation results (metrics) to Statsd endpoint. Note that this
         script assumes that all calculations required are performed by the database itself (via
         the queries used). If this is not desirable and processing should be moved to this script,
         separate functions can likely be developed for each query, but will likely make this
         script a bit more cumbersome/less general in nature.

NOTE: This script assumes that the MSSql, Graphite and Statsd instances have already been
      set up/configured for use and respective configurations exist in the config/.env file.
*/

// required libs
var sql = require('mssql');
var SDC = require('statsd-client');

/*************************** CONFIGURE QUERIES ***************************/
// configure the key/value hash entries following the example, in the format:
//   var queryMetrics = {
//     "SELECT COUNT(*) AS COUNT FROM <MY_MSSQL_QUERY>": "<MY_STATSD_METRIC_NAME>"
//   }
// the built-in functionality will take the key/value pairs and for each:
//   1. Run the SQL query, assuming a single record be returned (all calculations are
//      to be done on the SQL server instance and should result in a single "COUNT" result).
//   2. Send the single response metric to the statsd endpoint using the metric name
//      specified as the 'value' in the 'queryMetrics' hash entry
//
// WARNING: IT IS VERY LIKELY A GOOD IDEA TO ALWAYS USE '...with (NOLOCK)...' IN YOUR
//          QUERIES TO ENSURE YOU DO NOT LOCK THE TARGET DATABASE.
var queryMetrics = {
    "SELECT COUNT(*) AS COUNT FROM information_schema.tables WITH (NOLOCK) WHERE table_type = 'base table'": "nodejs.statsd.mssql.sample.tables"
};

// load all options/configs
require('dotenv').config({path: 'config/.env'});

var dbConfig = {
    user: process.env.DB_USER,
    password: process.env.DB_PASS,
    server: process.env.DB_HOST,
    port: process.env.DB_PORT,
    database: process.env.DB_NAME,
    stream: true
};

var statsdConfig = {
    host: process.env.STATSD_HOST,
    port: process.env.STATSD_PORT,
    debug: process.env.STATSD_DEBUG
};

// set up connection to statsd
var statsdConn = new SDC(statsdConfig);

// establish db connection and perform actions
sql.connect(dbConfig).then(function() {
    console.log("Connected to DB:", process.env.DB_NAME);

    // loop through and perform query/calculate functions desired
    for (var query in queryMetrics) {
        console.log("Performing query:", query);
        var request = new sql.Request();
        request.query(query);

        // received results - send along to statsd
        request.on('row', function(row) {
            var dataPoint = row["COUNT"];
            var metricName = queryMetrics[query];
            console.log("Received data for query:", dataPoint);
            console.log("Sending data point along to statsd metric:", metricName);

            // note that this is UDP interaction and will likely not throw errors if something goes wrong
            // (will fail silently)
            statsdConn.gauge(metricName, dataPoint);
        });

        // something bad happened - throw an error and continue to next query
        request.on('error', function(error) {
            console.error("Could not perform query:", error);
        });
    }

    // clean up connections
    sql.close();
    statsdConn.close();
}).catch(function(err) {
    console.error("Something went wrong with the DB connection: ", err);

    // clean up connections
    sql.close();
    statsdConn.close();
});
