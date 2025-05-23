#!/usr/bin/python3

import argparse
import requests
import json

parser = argparse.ArgumentParser(prog='port.py')
parser.add_argument('-H', '--host', help='<Required> ip address of target host')
parser.add_argument('-p', '--port', help='port number (1..x)')
parser.add_argument('-s', '--switch', help='state 0=Off, 1=On, 2=Toggle, 3=Reset')
parser.add_argument('-b', '--batch_delay', help='seconds between states')
parser.add_argument('-a', '--batch_states', nargs='+', help='multiple batch states (0=Off, 1=On, 2=Toggle), e.g.: 1 0')
parser.add_argument('-o', '--ovp', help='OVP numer, show OVP state (1..x)')
parser.add_argument('--ssl', help='use https connection', action="store_true")
parser.add_argument('--username', help='username for HTTP basic auth credentials')
parser.add_argument('--password', help='password for HTTP basic auth credemtials')

args = parser.parse_args()


class GudeDevice:
    @staticmethod
    def getJson(host, ssl, filename, params, username=None, password=None):
        if ssl:
            url = 'https://'
        else:
            url = 'http://'

        url += host + '/' + filename

        auth = None
        if username:
            auth = requests.auth.HTTPBasicAuth(username, password)

        r = requests.get(url, params=params, verify=False, auth=auth)
        print (f"GET {r.url}")
        print (f"<Response [{r.status_code }]>")
        print (f"{r.text}")

        if r.status_code == 200:
            return json.loads(r.text)
        else:
            raise ValueError("http request error {0}".format(r.status))

    @staticmethod
    def getPortJson(host, ssl=False, port=None, switch=None, batch=None, states=None, username=None, password=None):
        components = 1 + 512
        if port and (switch or batch and states):
            if batch and states:
                params = {'components': components, 'cmd': 5, 'p': port, 's': batch}
                for idx, state in enumerate(states):
                    params['a'+str(idx+1)] = state
            elif int(switch) != 3:
                params = {'components': components, 'cmd': 1, 'p': port, 's': switch}
            else:
                # s=3 does not exist, instead cmd=12 is used
                params = {'components': components, 'cmd': 12, 'p': port}
        else:
            params = {'components': components}
        return GudeDevice.getJson(host, ssl, 'statusjsn.js', params, username, password)

    def getPortState(self, port, use_cache=False):
        if port and port <= self.numPorts:
            if not use_cache:
                self.portJson = self.getPortJson(self.host, self.ssl, port, username=self.username, password=self.password)
            return self.portJson["outputs"][port-1]["state"]
        else:
            return None

    def getOvpState(self, ovp, use_cache=False):
        if ovp and ovp <= self.numBanks:
            if not use_cache:
                self.portJson = self.getPortJson(self.host, self.ssl, 1, username=self.username, password=self.password)
            return self.portJson["hardware"]["banks"][ovp-1]["fuse"]
        else:
            return None

    def __init__(self, host, ssl=False, port=None, switch=None, batch=None, states=None, username=None, password=None):
        self.host = host
        self.ssl = ssl
        self.username = username
        self.password = password
        self.portJson = self.getPortJson(host, ssl, port, switch, batch, states, username, password)
        self.numPorts = len(self.portJson["outputs"])
        self.numBanks = len(self.portJson["hardware"]["banks"])

if __name__ == "__main__":

    gudeDevice = GudeDevice(
        str(args.host), args.ssl,
        args.port, args.switch,
        args.batch_delay, args.batch_states,
        args.username, args.password
    )

    if args.ovp:
        print(gudeDevice.getOvpState(int(args.ovp), use_cache=True))
    elif args.port:
        print(gudeDevice.getPortState(int(args.port), use_cache=True))
    else:
        for p in range(1, gudeDevice.numPorts+1, use_cache=True):
            print(gudeDevice.getPortState(p))