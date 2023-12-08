import re
import os
import time
from py import test
import yaml
import pprint
import sys

sys.path.insert(1, os.path.join(sys.path[0],'..'))  # !!! PATH fo import with position 1!!!
# pprint.pprint(sys.path)

from ping3 import ping
from base_gns3 import Base_gns
from base_bm10 import Base_bm10

from rich import print
from rich.theme import Theme
from rich.console import Console
my_colors = Theme(
     #добавляет цветовую градацию для rich
    {
        "success":" bold green",
        "fail": "bold red",
        "info": "bold blue"
    }
)
console = Console(theme=my_colors)

with open("../command_cfg/value_bm10.yaml") as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Base_bm10(**device)


def check_int_pppoe(comm): 
    console.print("Test 1 \nОпределяем наличие настроенного интерфейса lan4 с РРРоЕ (есть ли конфиг вообще)",style='info')
    try:
        temp = r1.send_command(device, comm)
        if "lan4" in temp:
            return True
        else:
            return False
    except ValueError as err:
        return False
    

def check_ping_interf(ip_for_ping): # check ping Internet
    console.print("Test 2 \nПроверка доступности интерфейсов соседей, исп-ся в тесте с параметрами",style='info')
    try:
        res_ping_inet = r1.ping_ip(device,ip_for_ping)
        if "destination available" in res_ping_inet:
            console.print("Interface availeble ",style="success")
            return True
        else:
            console.print("Interface is not available ",style='fail')
            return False
    except ValueError as err:
        return False


def check_ip_pppoe_neib(comm): 
    console.print("Test 2 \nПроверка наличия нейбора, выдан ли адрес",style='info')
    try:
        temp = r1.send_command(device,comm)
        ip_peer = re.search(r'(?P<ip_peer>\d+.\d+.\d+.\d+) dev ppp0 proto',temp)
        ip_peer=ip_peer.group('ip_peer')
        ip_serv = re.search(r'ppp0 proto kernel scope link src (?P<ip_serv>\d+.\d+.\d+.\d+)',temp)
        if "ip_peer" !='ip_serv':
            print(f'Tunnel ok, ip client PPPoE: {ip_peer}, ip server PPPoE:',ip_serv.group('ip_serv'))
            return True
        else:
            if "state DOWN"in temp:
                print("interface exist, but state DOWN")
                return False
    except ValueError as err:
        return False



if __name__ =="__main__":
    print (check_ip_pppoe_neib('ip r'))