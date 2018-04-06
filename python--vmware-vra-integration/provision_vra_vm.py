#!/usr/bin/env python
#
# Purpose: Interface with the VMware vRA APIs to create a VM.
#

import requests
import yaml
import json
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# ignore annoyances
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# import configuration settings
with open('config/settings.yml', 'r') as yml:
    config = yaml.load(yml)

# some sane defaults
VRA_HEADERS = { 'accept': "application/json", 'content-type': "application/json" }

# utility to create headers with bearer token
# this is not terribly DRY, but it's better than doing it in each function
def create_headers(auth_token):
    headers = dict(VRA_HEADERS)
    headers['authorization'] = auth_token
    return headers

# get an auth bearer token
def get_token():
    url = "https://{}/identity/api/tokens".format(config['vra_host'])
    payload = '{{"username":"{}","password":"{}","tenant":"{}"}}'.format(config['vra_user'], config['vra_pass'], config['vra_tenant'])
    response = requests.request("POST", url, data=payload, headers=VRA_HEADERS, verify=False)

    # format bearer token into correct auth pattern
    j = response.json()['id']
    auth = "Bearer " + j
    return auth

# get an inventory of available catalog items and corresponding IDs
def get_inventory(auth_token):
    catalog_dict = {}
    url = "https://{}/catalog-service/api/consumer/entitledCatalogItems".format(config['vra_host'])

    # modify headers for bearer token
    headers = dict(VRA_HEADERS)
    headers['authorization'] = auth_token

    # perform request and parse results into dict
    response = requests.request("GET", url, headers=headers, verify=False)
    for i in response.json()['content']:
        item_name = i['catalogItem']['name']
        item_id = i['catalogItem']['id']
        catalog_dict[item_name] = item_id
    return catalog_dict

# get the JSON template for the blueprint execution
def get_template_json(auth_token, catalog_id):
    url = "https://{}/catalog-service/api/consumer/entitledCatalogItems/{}/requests/template".format(config['vra_host'], catalog_id)
    template_json = requests.request("GET", url, headers=create_headers(auth_token), verify=False)
    return template_json

# use the template JSON to create a VM from a blueprint
def create_vm_from_template(auth_token, catalog_id, template_json):
    url = "https://{}/catalog-service/api/consumer/entitledCatalogItems/{}/requests".format(config['vra_host'], catalog_id)
    vra_deploy = requests.request("POST", url, headers=create_headers(auth_token), data=template_json, verify=False)
    return vra_deploy.json()['id']

# get the status of a VM build using the ID of the VM
def get_vm_status(auth_token, request_id):
    url = "https://{}/catalog-service/api/consumer/requests/{}".format(config['vra_host'], request_id)
    request_status = requests.request("GET", url, headers=create_headers(auth_token), verify=False)
    return request_status

# get the resources associated with the request made (VM)
def get_vm_details(auth_token, request_id):
    url = "https://{}/catalog-service/api/consumer/requests/{}/resources".format(config['vra_host'], request_id)
    request_resources = requests.request("GET", url, headers=create_headers(auth_token), verify=False)

    # get the Destroy ID and VM Name using list comprehension
    meta_dict = [element for element in request_resources.json()['content'] if element['providerBinding']['providerRef']['label'] == 'Infrastructure Service'][0]
    destroy_id = meta_dict['id']
    vm_name = meta_dict['name']

    # get the VM IP address using list comprehension
    vm_data = [element for element in meta_dict['resourceData']['entries'] if element['key'] == 'ip_address'][0]
    vm_ip = vm_data['value']['value']

    return (destroy_id, vm_name, vm_ip)

#################################
# main execution
# Steps:
#   1. Get Bearer token.
#   2. Get an inventory of available catalog items.
#   3. Get specific catalog item ID based on inventory item name.
#   4. Get template JSON for catalog item ID.
#   5. Request VM using template JSON.
#   6. Return Destroy ID, VM Name, and VM IP Address.
#################################

print "############################################################"
print "Getting a bearer token..."
auth_token = get_token()

print "############################################################"
print "Getting an inventory of available catalog items and finding '{}'...".format(config['vra_bp_name'])
inventory = get_inventory(auth_token)
catalog_id = inventory[config['vra_bp_name']]

print "############################################################"
print "Getting the template JSON for the requested catalog item ID..."
template_json = get_template_json(auth_token, catalog_id)

print "############################################################"
print "Making the request for the VM to be created..."
request_id = create_vm_from_template(auth_token, catalog_id, template_json)
print("Request submitted - ID: {}".format(request_id))

print "############################################################"
print "Checking on the status of the VM build request..."
timer = 0
while True:
    print('Waiting for VM...')
    status = get_vm_status(auth_token, request_id)

    # check if we've exceeded the timeout
    if timer >= config['provision_timeout_seconds']:
        raise Exception("Timeout attempting to wait {} seconds for VM to finish provisioning!".format(config['provision_timeout_seconds']))
    elif status.json()['state'] == config['provision_success']:
        print("VM is ready - took roughly {} seconds".format(timer))
        break

    # iterate on wait timing
    time.sleep(15)
    timer += 15

print "############################################################"
print "Getting VM information..."
destroy_id, vm_name, vm_ip = get_vm_details(auth_token, request_id)
print("Destroy ID: {}".format(destroy_id))
print("VM Name: {}".format(vm_name))
print("VM IP: {}".format(vm_ip))
