#!/usr/bin/env python
#
# Purpose: Publish a message to a Slack channel as specified in the
#          config/settings.json file - make sure you invite the bot user
#          to the channel first.
#
# some functionality taken from this page:
#   https://slack.dev/python-slackclient/basic_usage.html
#

import yaml
import logging
from slack import WebClient
from slack.errors import SlackApiError

# obtain the configuration settings
with open('config/settings.yaml', 'r') as yml:
  config = yaml.load(yml, Loader=yaml.FullLoader)['slack']

client = WebClient(token=config['bot_token'])

# attempt to publish a message to the endpoint
try:
  response = client.chat_postMessage(
    channel=config['channel'],
    blocks=[
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "Hello World!"
        }
      }
    ]
  )
except SlackApiError as e:
  print("ERROR: {}".format(e.response))
