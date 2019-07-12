#!/usr/bin/env python
#
# Make an HTTP request to a URL endpoint and parse response as JSON.
#

import requests
import json

def run():
    res = requests.get('https://jsonplaceholder.typicode.com/todos/1')
    resp_json = json.loads(res.text)
    print(resp_json)

if __name__ == '__main__':
    run()
