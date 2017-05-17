#!/usr/bin/env python
#
# This is a script to demonstrate obtaining a secret from Secret Server using the SOAP API interaction
# as defined by the WSDL. This code has very minimal error handling and only prints the JSON response
# generated from a successful call to the server itself (parsing the data and use of the JSON object
# is assumed to be the responsibility of the developer)

from pysimplesoap.client import SoapClient
import yaml
import json

# obtain the configuration information
with open('config/settings.yml', 'r') as yml:
  config = yaml.load(yml)['secret_server']

# create the client for WSDL interaction
client = SoapClient(wsdl = config['wsdl_url'], trace = False)

# perform a request for an auth token, and raise an exception if none can be obtained
response   = client.Authenticate(username = config['auth']['username'], password = config['auth']['password'], domain = config['auth']['domain'])
auth_token = response['AuthenticateResult']['Token']

if auth_token is None:
  raise Exception("An authentication exception has occurred: %s" % response['AuthenticateResult']['Errors'])

# attempt to get the secret information
# handling of errors is a bit different than the token retrieval because the response signature does not
# guarantee that the Secret key will be present (whereas the Token response guarantees the Token key
# will be present even if it is set to None)
response = client.GetSecret(token = auth_token, secretId = config['secret_id'])

if 'Secret' in response['GetSecretResult']:
  secret = response['GetSecretResult']['Secret']
else:
  raise Exception("Could not obtain the secret: %s" % response['GetSecretResult']['Errors'])

# print the response - this is only for helpful debugging and not a necessary part of the request/response flow
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "PARAMETERS:"
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "WSDL URL:      %s" % config['wsdl_url']
print "Secret ID:     %s" % config['secret_id']
print "Auth Username: %s" % config['auth']['username']
print "Auth Domain:   %s" % config['auth']['domain']
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "RESULT FROM REQUEST..."
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "Auth Token:    %s" % auth_token
print "Secret Data: "
print json.dumps(secret, sort_keys=True, indent=4, separators=(',', ': '))
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
