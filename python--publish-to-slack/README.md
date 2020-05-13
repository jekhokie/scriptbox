# Publish to Slack

Simple Python application to publish messages to a Slack channel. When running the script, a simple
"Hello World!" message will be sent to the Slack channel specified in your configuration.

## Prerequisites - Slack App

First, create a BOT OAuth token for your Slack workspace - this requires creating and publishing an
app to your workspace, which will then expose the BOT token. Copy this value as it is needed in the
`config/settings.json` file you will create later.

Ensure that your Slack app has the following "Bot Token Scopes" defined/permitted:

- `chat:write`
- `chat:write.customize`

Next, publish your app to your workspace.

Finally, invite the Slack App bot to the channel where you wish to publish messages via the
`/invite @botusername` command in Slack.

## Prerequisites - Python

Install easy_install, pip and virtualenv. Then, clone this repository and navigate to this example:

```bash
$ git clone https://<git_location>/scriptbox.git
$ cd scriptbox/python--publish-to-slack/
```

Install the required environment and libraries:

```bash
$ virtualenv --no-site-packages --distribute .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

Create a configuration file from the sample and specify the values for your specific environment to
include the Bot Token and associated channel ID, which can be either a Channel ID or specific User ID
(where each are the ID that exists at the tail end of the URL for the channel or user, respectively).

```bash
$ cp config/settings.json.sample config/settings.json
# edit the config/settings.json file for your settings
```

## Usage

Now that the configurations are in place, run the script to publish a message:

```bash
$ python publish_message.py
# you should see a message posted to the slack channel you specified
```
