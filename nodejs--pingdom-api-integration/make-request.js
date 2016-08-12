/*
Purpose: Interaction with the Pingdom API to obtain a list of known accounts.

NOTE: This script assumes that the account being used to interact with is not the same
      account used to perform the requests. In other words, it assumes the "Multi-User
      Authentication" section of the API documentation:
          https://www.pingdom.com/resources/api#multi-user+authentication
*/

var request = require('request');

// load all options
require('dotenv').config({path: 'config/.env'});

// options for the HTTP request being made
var options = {
    auth: {
        user: process.env.PINGDOM_USERNAME,
        pass: process.env.PINGDOM_PASSWORD
    },
    uri: process.env.PINGDOM_API_URL + '/users',
    method: 'GET',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'App-Key': process.env.PINGDOM_APP_KEY,
        'Account-Email': process.env.PINGDOM_ACCOUNT_EMAIL
    }
};

// make the request desired
request(options, function(error, response, body) {
	var jsonResponse;

    // handle non-API unaccounted for exceptions
    if (error) {
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
    var userList = jsonResponse.users;
    for (var user in userList) {
        console.log(userList[user]);
    }
});
