#!/usr/bin/python3

import argparse
import requests
import json

parser = argparse.ArgumentParser(prog='port.py')
parser.add_argument('-H', '--host', help='ip address of target host')
parser.add_argument('-p', '--port', help='port number (1..x)')
parser.add_argument('-s', '--switch', help='state 0=Off, 1=On, 2=Toggle, 3=Reset')
parser.add_argument('-o', '--ovp', help='OVP numer, show OVP state (1..x)')
parser.add_argument('--ssl', help='use https connection', action="store_true")
parser.add_argument('--username', help='username for HTTP basic auth credentials')
parser.add_argument('--password', help='password for HTTP basic auth credemtials')

args = parser.parse_args()


class GudeDevice:
    def getJson(self, host, ssl, filename, params, username=None, password=None):
        if ssl:
            url = 'https://'
        else:
            url = 'http://'

        url += host + '/' + filename

        auth = None
        if username:
            auth = requests.auth.HTTPBasicAuth(username, password)

        r = requests.get(url, params=params, verify=False, auth=auth)
        print (f"{r.url}")

        if r.status_code == 200:
            return json.loads(r.text)
        else:
            raise ValueError("http request error {0}".format(r.status))

    def getPortJson(self, host, ssl, port=None, switch=None, username=None, password=None):
        components = 1 + 512
        if (port is not None and switch is not None):
            if int(switch) != 3:
                params = {'components': components, 'cmd':1, 'p':port, 's':switch}
            else:
                params = {'components': components, 'cmd':12, 'p':port}
        else:
            params = {'components': components}
        return self.getJson(host, ssl, 'statusjsn.js', params, username, password)

    def getPortState(self, port):
        if port and port <= self.numPorts:
            return self.portJson["outputs"][port-1]["state"]
        else:
            return None

    def getOvpState(self, ovp):
        if ovp and ovp <= self.numBanks:
            return self.portJson["hardware"]["banks"][ovp-1]["fuse"]
        else:
            return None

    def __init__(self, host, ssl, port=None, switch=None, username=None, password=None):
        self.portJson = self.getPortJson(host, ssl, port, switch, username, password)
        self.numPorts = len(self.portJson["outputs"])
        self.numBanks = len(self.portJson["hardware"]["banks"])


gudeDevice = GudeDevice(
    str(args.host), args.ssl,
    args.port, args.switch,
    args.username, args.password
)

if args.ovp:
    print(gudeDevice.getOvpState(int(args.ovp)))
elif args.port:
    print(gudeDevice.getPortState(int(args.port)))
else:
    for p in range(1, gudeDevice.numPorts+1):
        print(gudeDevice.getPortState(p))
