#!/usr/bin/env python3
import requests
from ipaddress import IPv4Address, IPv4Network

response = requests.get("https://www.cloudflare.com/ips-v4")
ranges = response.text
# print(ranges)
nets = list()
for line in ranges.splitlines():
    net = IPv4Network(line)
    nets.append(net)
print(nets)
for net in nets:
    if IPv4Address("103.22.200.1") in net:
        print("found")
        break
