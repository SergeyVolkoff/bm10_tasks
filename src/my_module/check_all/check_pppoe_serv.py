import re
import os
import time
from py import test
import yaml
import pprint
import sys

from cfg_bm10 import Cfg_bm10

sys.path.insert(1, os.path.join(sys.path[0],'..'))  # !!! PATH fo import with position 1!!!
# pprint.pprint(sys.path)

from ping3 import ping
from base_gns3 import Base_gns
from base_bm10 import Base_bm10

from rich import print
from rich.theme import Theme
from rich.console import Console
from constants import (
    DEVICE_BM10,
    RESET_CONFIG_COMMAND,
    CONSOLE,
)

r1 = Cfg_bm10(**DEVICE_BM10)

def check_int_pppoe(comm): 
    CONSOLE.print("Test 1 \nОпределяем наличие настроенного интерфейса lan4 с РРРоЕ (есть ли конфиг вообще)",style='info')
    try:
        temp = r1.send_command(DEVICE_BM10, comm)
        if "lan4" in temp:
            return True
        else:
            return False
    except ValueError as err:
        return False
    

def check_ping_interf(ip_for_ping): # check ping Internet
    CONSOLE.print("Test 2 \nПроверка доступности интерфейсов соседей, исп-ся в тесте с параметрами",style='info')
    try:
        res_ping_inet = r1.ping_ip(DEVICE_BM10,ip_for_ping)
        if "destination available" in res_ping_inet:
            CONSOLE.print("Interface availeble ",style="success")
            return True
        else:
            CONSOLE.print("Interface is not available ",style='fail')
            return False
    except ValueError as err:
        return False


def check_ip_pppoe_neib(comm): 
    CONSOLE.print("Test 3 \nПроверка наличия нейбора, выдан ли адрес",style='info')
    try:
        temp = r1.send_command(DEVICE_BM10,comm)
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