# Sonos Query

This is a simple script to interact with a Sonos device using SOAP. It is absolutely not full-fledged
functionality, but a way to store something I discovered without needing to re-invent this if I decide
to pick it up in the future. There is also no guarantee this will work with future/previous versions of
Sonos devices from what it was originally written for.

## Prerequisites

Install pip and virtualenv. Then, clone this repository and navigate to this example:

```bash
$ git clone https://<git_location>/scriptbox.git
$ cd scriptbox/python--sonos-query
```

Install the required environment and libraries (assumes Python 3 and virtualenv are installed):

```bash
$ python3 -m virtualenv .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

## Run Script

In the script is a hard-coded IP address for a Sonos device you wish to query (yes, should be extracted
as a configuration file parameter - maybe sometime in the future). Update this to be one of your Sonos
devices and then run the script:

```bash
$ python query_sonos.py
```

You should see XML output that corresponds to a query made against the Sonos SOAP endpoint and collected
some information about the device.

That's it (currently) - again, this is just for future reference in case I need it again.
