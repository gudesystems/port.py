#!/usr/bin/python

import argparse
import requests
import json

parser = argparse.ArgumentParser(prog='check_gude')
parser.add_argument('-H', '--host', help='ip address of target host')
parser.add_argument('-p', '--port', help='port number (1..x)')
parser.add_argument('-s', '--switch', help='state 0=Off, 1=On')
parser.add_argument('--ssl', help='use https connection', action="store_true")
parser.add_argument('--username', help='username for HTTP basic auth credentials')
parser.add_argument('--password', help='password for HTTP basic auth credemtials')

args = parser.parse_args()


class GudeDevice:
    def getPortJson(self, host, ssl, port=None, switch=None, username=None, password=None):
        if ssl:
            url = 'https://'
        else:
            url = 'http://'

        url += host + '/' + 'statusjsn.js'

        auth = None
        if username:
            auth = requests.auth.HTTPBasicAuth(username, password)

        if (port is not None and switch is not None):
            params = {'components':1, 'cmd':1, 'p':port, 's':switch}
        else:
            params = {'components': 1}

        r = requests.get(url, params=params, verify=False, auth=auth)

        if r.status_code == 200:
            return json.loads(r.text)
        else:
            raise ValueError("http request error {0}".format(r.status))

    def getPortState(self, port):
        port = int(port)-1
        if port <= self.numPorts:
            return self.portJson["outputs"][port]["state"]
        else:
            return None

    def __init__(self, host, ssl, port=None, switch=None, username=None, password=None):
        self.portJson = self.getPortJson(host, ssl, port, switch, username, password)
        self.numPorts = len(self.portJson["outputs"])


gudeDevice = GudeDevice(
    str(args.host), args.ssl,
    args.port, args.switch,
    args.username, args.password
)

if args.port:
    print(gudeDevice.getPortState(args.port))
else:
    for p in range(0, gudeDevice.numPorts):
        print(gudeDevice.getPortState(p))
