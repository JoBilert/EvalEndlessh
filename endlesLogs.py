import matplotlib.pyplot as plt
import numpy as np
import os

# from urllib.request import urlopen
# from json import load

import IP2Location

import paramiko
from scp import SCPClient

import pandas as pd

from pandas.core.indexes.base import Index

database = IP2Location.IP2Location(os.path.join("/config/EvalEndlessh/data", "IPV6-COUNTRY.BIN"))


def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

def recon(ip):
    rec = database.get_all(ip)
    return rec
    
def parseFile():
    lines = []
    date = []
    time = []
    host = []
    country = []
    index = []

    with open('logs.txt', 'r') as f:
        for line in f:
            lines.append(line.strip())

    for line in lines:
        if "ACCEPT" in line:
            elements = line.split()
            index.append(elements[2])
            date.append(elements[0])
            time.append( elements[1][:8])
            host.append(elements[4][12:])
            recInfo = recon(elements[4][12:])
            country.append(recInfo.country_long)
            
    df = pd.DataFrame(list(zip(date, time, host, country)), index = index, columns=['Date', 'Time', 'IP', 'Country'])    
    return df
   
ssh = createSSHClient("192.168.2.177", 2244, "pi", "08.Mai99")
scp = SCPClient(ssh.get_transport())
scp.get("/home/pi/endlessh/logs/endlessh/current", "logs.txt")
data = parseFile()
data_clean = pd.DataFrame(data['Country'].value_counts(dropna=False))
data_clean = data_clean.reset_index()
data_clean.plot.bar(x='index', y='Country')
plt.show()
print (data_clean)