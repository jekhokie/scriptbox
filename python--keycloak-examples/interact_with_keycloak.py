#!/usr/bin/env python
#
# Small example of how to integrate with the Keycloak open source identity
# and access management (IAM) software. Most of this code is completely
# possible to obtain online, but serves as a decent starting point.
#
# Assumptions:
#   - Keycloak software is running/listening on IP 10.11.13.50 and port 8080
#   - There is a user with name 'demo' and password 'demo' in the realm 'demo'
#   - A client and secret has been created (see/update below configurations)

from keycloak import KeycloakOpenID

# environment configs
server_url = 'http://10.11.13.50:8080/auth/'
user = 'demo'
password = 'demo'
realm_name = 'demo'

client_id = 'demo_client'
client_secret = 'df0eb620-53af-4c62-ae41-71941cbfa1a4'

# interact with the software in various ways
keycloak_openid = KeycloakOpenID(server_url=server_url, realm_name=realm_name, client_id=client_id, client_secret_key=client_secret)
print("OPENID:")
print(keycloak_openid)

config_well_know = keycloak_openid.well_know()
print("WELL KNOW:")
print(config_well_know)

token = keycloak_openid.token(user, password)
print("TOKEN:")
print(token)

user_info = keycloak_openid.userinfo(token['access_token'])
print("USER INFO:")
print(user_info)

certs = keycloak_openid.certs()
print("CERTS:")
print(certs)
