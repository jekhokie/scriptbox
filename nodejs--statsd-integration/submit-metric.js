/*
Purpose: Interaction with the Statsd product to submit metrics. It sends 1 data point every
         1 second, which means Graphite storage needs to be configured according to the
         settings in the included README.

NOTE: This script assumes that the statsd instance has already been set up/configured
      for use and respective configurations exist in the config/.env file.
*/

// load statsd library
var SDC = require('statsd-client');

// load all options
require('dotenv').config({path: 'config/.env'});

// variable init
var min = 0;        // minimum metric value
var max = 1000;     // maximum metric value

// create statsd instance to interact with
sdc = new SDC({host: process.env.STATSD_HOST, port: process.env.STATSD_PORT, debug: process.env.DEBUG_MODE});

// send a metric to the statsd instance specified
var sendMetric = function() {
    var randNum = Math.random() * (max - min) + min;
    sdc.gauge(process.env.STATSD_COUNTER_NAME, Math.round(randNum));
};

// send METRIC_COUNT metrics, with 1 second delays between
(function metricProc (i) {
    setTimeout(function () {
        sendMetric();
        if (--i) metricProc(i);
    }, 1000)
})(process.env.METRIC_COUNT);

// close statsd instance connection
sdc.close();
