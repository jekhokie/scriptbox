/*
Purpose: Interaction with the PagerDuty API to obtain a list of services and enumerate
         the support level of each. This script could easily be updated to obtain
         information about any of the resources available through the PagerDuty API.

    NOTE: This request is for all services returned with time corresponding to
          EST and has a limit of 100. If you have more than 100 services in your
          PagerDuty account, you will likely need to handle pagination as the
          return object will likely contain something like "more: true" for the
          additional services beyond the initial 100 pulled.

    ADDL NOTE: This script assumes the following rules (and assumes that support hours
               are available/part of the capabilities of the queried account, which is
               only possible via the Standard/Pro licenses as of this script creation):

                 If "incident_urgency_rule" type == "constant" and "incident_urgency_rule" urgency == "high":
                    Support Hours = 24x7x365
                 If "incident_urgency_rule" type == "constant" and "incident_urgency_rule" urgency != "high":
                    Support Hours = None
                 If "incident_urgency_rule" type == "use_support_hours":
                    If "incident_urgency_rule" during_support_hours.urgency == "high":
                        Support Hours = Parse "support_hours" object in response
                    If "incident_urgency_rule" during_support_hours.urgency == "low":
                        Support Hours = 24x7x365
*/

var request = require('request');

// load all options
require('dotenv').config({path: 'config/.env'});

// options for the HTTP request being made
var options = {
    method: 'GET',
    dataType: 'json',
    uri: process.env.PAGERDUTY_API_URL + '/services?time_zone=EST&limit=100',
    headers: {
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Authorization': 'Token token=' + process.env.PAGERDUTY_API_KEY
    }
};

// print the support hours for a particular service
// to the screen
function printServiceSupportHours(svc) {
    var svcSupport = svc.name + ': ';
    var svcRule = svc.incident_urgency_rule;

    // determine the support hours for the service
    if (svcRule && svcRule.type === 'constant') {
        if (svcRule.urgency == 'high') {
            svcSupport += '(24x7x365)';
        } else {
            svcSupport += ' (None)';
        }
    } else if (svcRule && svcRule.type === 'use_support_hours') {
        // parse the 'days of the week' based on array of days
        var daysOfWeek = '';
        var days = svc.support_hours.days_of_week.sort();
        if (days.length == 7) {
            daysOfWeek = 'Every Day';
        } else if (days.sort().join(',') === '1,2,3,4,5') {
            daysOfWeek = 'Monday - Friday';
        } else {
            // no easy pattern, parse specific days - this is terrible
            // and should be done a different way, but since the array
            // is already sorted, we'll just do it
            for (var i = 0; i < days.length; i++) {
                switch(days[i]) {
                    case 1:
                        daysOfWeek += 'Monday';
                        break;
                    case 2:
                        daysOfWeek += 'Tuesday';
                        break;
                    case 3:
                        daysOfWeek += 'Wednesday';
                        break;
                    case 4:
                        daysOfWeek += 'Thursday';
                        break;
                    case 5:
                        daysOfWeek += 'Friday';
                        break;
                    case 6:
                        daysOfWeek += 'Saturday';
                        break;
                    case 7:
                        daysOfWeek += 'Sunday';
                        break;
                }

                if ((i + 1) < days.length) {
                    daysOfWeek += ', ';
                }
            }
        }

        // determine if we are handling critical during defined hours or outside defined hours
        if (svcRule.during_support_hours.urgency === 'high') {
            svcSupport += ' (' + 
                           svc.support_hours.start_time + ' - ' +
                           svc.support_hours.end_time + ' EST, ' +
                           daysOfWeek + ')';
        } else {
            svcSupport += ' (24x7x365)';
        }
    } else {
        svcSupport += ' (UNKNOWN)';
    }

    // output the service and support hours
    console.log(svcSupport);
}

// perform http requests and parse results
function callback(error, response, body) {
	var jsonResponse;

    // handle non-API unaccounted for exceptions
    if (error || response.statusCode != 200) {
        return console.error('Request failed', error);
    }

    // attempt to convert the response to JSON
    try {
        jsonResponse = JSON.parse(body);
    } catch (e) {
        return console.error('Conversion of response to JSON failed', e);
    }

    // check if the API returned an error
    if (jsonResponse.error !== undefined) {
        console.error('An error was reported from the site', jsonResponse.error);
    }

    // seems like we received a valid response with information - start parsing
    var serviceList = jsonResponse.services;
    for (var i = 0; i < serviceList.length; i++) {
        printServiceSupportHours(serviceList[i]);
    }
}

// make the request desired
request(options, callback);
