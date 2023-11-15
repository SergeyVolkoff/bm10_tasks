
import re
import sys
import os
import time
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
sys.path.insert(1, os.path.join(sys.path[0],'..'))  # !!! PATH fo import with position 1!!!

from base_bm10 import Base_bm10
from ping3 import ping
from base_gns3 import Base_gns
from base_bm10 import Base_bm10
from gns3fy import *

from rich import print
from rich.theme import Theme
from rich.console import Console
my_colors = Theme( #добавляет цветовую градацию для rich
    {
        "success":"bold green",
        "fail":"bold red",
        "warning":"bold yellow"
    }
)
console = Console(theme=my_colors)

with open("/home/ssw/Documents/bm10_tasks/src/my_module/command_cfg/value_bm10.yaml") as f:
    temp = yaml.safe_load(f)
    for t in temp:
        device = dict(t)
        r1 = Base_bm10(**device)


def check_enable_ospfv2():
 
    '''Проверка enable OSPFv2'''

    try:
        temp = r1.send_command(device, 'uci show ospf.@ospf[0].enabled')
        if "='1'" in temp:
            console.print("OSPFv2 - enable!",style="success")
            return True
        else:
            
            return False
    except ValueError as err:
        return False



def check_route_ospfv2_net():
    # ф-я в цикле переберет список маршрутов, если нужного нет - вернет false
    try:
        return_ip_route = r1.send_command(device, "ip route")
        list_iproute=('192.168.10.0/24',
                      '192.168.20.0/24',
                      '200.1.10.0/24 ',
                      '200.1.20.0/24 ',
                     
                      )
        i=0
        for ip in list_iproute:
            if ip  in return_ip_route:
                i+=1
                console.print(f"Ip route {ip} ok!",style="success")
            else:
                if ip  not in return_ip_route:
                    console.print(f"No ip route {ip} ",style='fail')
        if i==4:
            return True
        else:
            return False
    except ValueError as err:
        return False
    

def check_ping_interf(ip_for_ping): # check ping Internet
    try:
        res_ping_inet = r1.ping_ip(device,ip_for_ping)
        print(res_ping_inet)
        if "destination available" in res_ping_inet:
            console.print("Interface availeble, OSPFv2 OK",style="success")
            return True
        else:
            console.print("Interface is not available, OSPFv2 bad ",style='fail')
            return False
    except ValueError as err:
        return False
    