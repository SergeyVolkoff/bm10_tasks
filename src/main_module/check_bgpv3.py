import re
import time
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from base_bm10 import Base_bm10

with open("command_cfg/value_bm10.yaml") as f:
    temp = yaml.safe_load(f)
    for t in temp:
        device = dict(t)
        r1 = Base_bm10(**device)


def check_enable_bgpv3():
    try:
        temp = r1.send_command(device, 'uci show bgp.@bgp[0].enabled')
        if "='1'" in temp:
            print("BGP - enable!")
            return True
        else:
            return False
    except ValueError as err:
        return False
    

def check_redistr_kernel():
    try:
        temp = r1.send_command(device, 'uci show bgp.@bgp[0].redistribute_kernel')
        if " kernel" in temp:
            print("Redistribute_kernel - enable!")
            return True
        else:
            return False
    except ValueError as err:
        return False
    
def check_redistr_connected():
    try:
        temp = r1.send_command(device, 'uci show bgp.@bgp[0].redistribute_connected')
        if " connected" in temp:
            print("Redistribute_connected - enable!")
            return True
        else:
            return False
    except ValueError as err:
        return False
    
def check_redistr_static():
    try:
        temp = r1.send_command(device, 'uci show bgp.@bgp[0].redistribute_static')
        if " static" in temp:
            print("Redistribute_static - enable!")
            return True
        else:
            return False
    except ValueError as err:
        return False
    

def check_route10_bgpv3():
    try:
        temp = r1.send_command(device, "ip route")
        if "200.1.10.0/24 via 192.168.10.2" in temp:
            print("Ip route 200.1.10.0/24 to host ok!")
            return True
        else:
            return False
    except ValueError as err:
        return False
    

def check_route20_bgpv3():
    try:
        temp = r1.send_command(device, "ip route")
        if "200.1.20.0/24 via 192.168.20.2" in temp:
            print("Ip route 200.1.20.0/24 to host ok!")
            return True
        else:
            return False
    except ValueError as err:
        return False

def check_ping_interf(ip_for_ping): # check ping neighbor
    try:

        res_ping_inet = r1.ping_ip(device,ip_for_ping)
        print(res_ping_inet)
        if "destination available" in res_ping_inet:
            print("Interface  availeble, BGP OK")
            return True
        else:
            print("Interface 200- not available, BGP bad ")
            return False
    except ValueError as err:
        return False