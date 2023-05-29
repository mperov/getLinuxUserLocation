#!/bin/env python3

import sys
import json
import urllib.request
import paramiko
import logging
import time
from argparse import ArgumentParser

GEO_IP_API_URL = 'http://ip-api.com/json/'
SLEEP=3

def getTable(host, user, port, filename, old):
    k = paramiko.RSAKey.from_private_key_file(filename)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        if old:
            ssh.connect(hostname=host, username=user, pkey=k, port=port, disabled_algorithms=dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"]))
        else:
            ssh.connect(hostname=host, username=user, pkey=k, port=port)
    except:
        print("ERROR: ssh connection")
        return ["ERROR: ssh connection"]
    try:
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('/opt/whereFrom')
    except:
        print("ERROR: running /opt/whereFrom")
        return ["ERROR: running /opt/whereFrom"]
    return ssh_stdout.readlines()

def getInfo(ipAddr = ''):
    if ipAddr != '':
        try:
            req = urllib.request.Request(GEO_IP_API_URL + ipAddr)
            response = urllib.request.urlopen(req).read()
        except:
            return 'Unknown'
        json_response = json.loads(response.decode('utf-8'))
        symbols = ":\t "
        if len(ipAddr) == 15:
            symbols = ": "
        try:
            return ipAddr + symbols + json_response['country'] + '/' + json_response['city'] + ' - ' + json_response['isp']
        except:
            return 'Unknown'
    return ''

def show(host = '127.0.0.1', user='root', port=22, filename='/home/coder/.ssh/id_rsa', old=False, console=False, debug=False):
    lines = getTable(host, user, port, filename, old=old)
    pairs = []
    output=""
    for line in lines:
        user = line.split('\t\t')[0]
        try:
            ip = line.split('\t\t')[1].split('\n')[0]
        except:
            ip = '0.0.0.0'
        if line[:6] == "ERROR:":
            output += line
            continue
        info = getInfo(ip)
        if info != '':
            if not (user, ip) in pairs:
                if len(user) > 15:
                    if console:
                        print('{:<12}\t{:<12}'.format(user, info))
                    else:
                        if debug:
                            print('{:<12}\t{:<12}'.format(user, info))
                        output += '{:<12}\t{:<12}'.format(user, info) + '\n'
                else:
                    if console:
                        print('{:<12}\t\t{:<12}'.format(user, info))
                    else:
                        if debug:
                            print('{:<12}\t{:<12}'.format(user, info))
                        output += '{:<12}\t\t{:<12}'.format(user, info) + '\n'
                pairs.append((user, ip))
        time.sleep(SLEEP)
    return output

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-hi", "--hostIP", dest="hostIP",
                        help="contain IP address your server")
    parser.add_argument("-p", "--port", dest="port", default=22,
                        help="contain ssh port")
    parser.add_argument("-u", "--user", dest="user",
                        help="contain username with sudo rules")
    parser.add_argument("-k", "--private-key", dest="key",
                        help="contain path to private key file")
    parser.add_argument("-d", "--debug", action='store_true',
                        help="this option enables debug mode")
    parser.add_argument("-o", "--old", action='store_true',
                        help="this option for old Linux distributions")
    args = parser.parse_args()
    debug = args.debug
    if args.hostIP and args.user and args.port and args.key:
        if debug:
            logging.basicConfig()
            logging.getLogger("paramiko").setLevel(logging.DEBUG)
        print(show(args.hostIP, args.user, port=int(args.port), filename=args.key, old=args.old, console=True))
    else:
        parser.print_help()
