#!/usr/bin/env python

import requests
from xml.dom.minidom import parseString

# configure IP for a Sonos device
SONOS_IP = '192.168.1.71'

# set up some configurations - including request for Control
# endpoint which shows things such as currently playing track
# and info about it
sonos_soap_url = "http://{}:1400/MediaRenderer/AVTransport/Control".format(SONOS_IP)
sonos_soap_headers = {'SOAPAction': 'urn:schemas-upnp-org:service:AVTransport:1#GetPositionInfo', 'Content-Type': 'text/xml; charset=UTF-8'}
sonos_soap_envelope = """<?xml version="1.0"?>
                         <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                           <s:Body>
                             <u:GetPositionInfo xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
                               <InstanceID>0</InstanceID>
                               <Channel>Master</Channel>
                             </u:GetPositionInfo>
                           </s:Body>
                         </s:Envelope>
"""

try:
    # obtain root XML
    print("Querying Sonos device...")
    sonos_response = requests.post(sonos_soap_url, data=sonos_soap_envelope, headers=sonos_soap_headers)
    sonos_response_xml = parseString(sonos_response.content)

    # print the entire XML
    print("\n-----------------------------------")
    print("CONTROL ENDPOINT XML")
    print("-----")
    print(sonos_response_xml.toprettyxml(indent="  "))
    print("-----------------------------------")

    print("Deconstructing track information...")
    track_metadata_str = sonos_response_xml.getElementsByTagName('TrackMetaData')[0].firstChild.nodeValue
    track_metadata = parseString(track_metadata_str)
    print("\n-----------------------------------")
    print("TRACK METADATA XML")
    print("-----")
    print(track_metadata.toprettyxml(indent="  "))
    print("-----------------------------------")
except:
    print("Failed to get information from Sonos device")
