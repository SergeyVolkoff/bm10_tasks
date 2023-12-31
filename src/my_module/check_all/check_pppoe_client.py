import re
import os
import time
from py import test
import yaml
import pprint
import sys

sys.path.insert(1, os.path.join(sys.path[0],'..'))  # !!! PATH fo import with position 1!!!
# pprint.pprint(sys.path)

from base_gns3 import Base_gns
from base_bm10 import Base_bm10
from cfg_bm10 import Cfg_bm10
from rich import print


with open("../command_cfg/value_bm10.yaml") as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Base_bm10(**device)

def check_int_pppoe_cl(comm): 
    Cfg_bm10.console.print("Test 1 \nОпределяем наличие настроенного интерфейса wan с РРРоЕ (есть ли конфиг вообще)",style='info')
    try:
        temp = r1.send_command(device, comm)
        if "pppoe" in temp:
            return True
        else:
            return False
    except ValueError as err:
        return False
    
def check_ip_pppoe(comm): 
    Cfg_bm10.console.print("Test 2 \nОпределяем наличие ip на интерфейсе wan с РРРоЕ",style='info')
    try:
        temp = r1.send_command(device,comm)
        temp2 = re.search(r'\s+inet (?P<intf>\d+.\d+.\d+.\d+) peer (.{0,})pppoe-wan',temp).group()
        output = re.search(r'\s+inet (?P<ip_int>\d+.\d+.\d+.\d+) peer (?P<ip_peer>\d+.\d+.\d+.\d+).{0,}pppoe-wan', temp)
        #ip_per=output.group('ip_peer')
        if "inet" in temp2:
            print('Tunnel ok, ip client:',output.group('ip_int'),', ip peer(serv):',output.group('ip_peer'))
            return True
        else:
            if "state DOWN"in temp2:
                print("interface exist, but state DOWN")
                return False
    except ValueError as err:
        return False

def check_ping_inet(): # check ping Internet
    Cfg_bm10.console.print("Test 3 \n Определяем доступность инета (8.8.8.8), в тестах эта проверка отключена")
    try:
        res_ping_inet = r1.ping_inet(device)
        print(res_ping_inet)
        if "destination available" in res_ping_inet:
            print("Inet(8.8.8.8) availeble, PPPoE OK")
            return True
        else:
            print("Inet(8.8.8.8)- not available, PPPoE bad ")
            return False
    except ValueError as err:
        return False

'''
используется параметризация!!
'''
def check_ping_interface(ip_for_ping): # check ping Internet
    Cfg_bm10.console.print("Test 4 \nПроверка доступности интерфейсов, исп-ся в тесте с параметрами",style='info')
    try:
        res_ping_inet = r1.ping_ip(device,ip_for_ping)
        if "destination available" in res_ping_inet:
            Cfg_bm10.console.print("Interface availeble ",style="success")
            return True
        else:
            Cfg_bm10.console.print("Interface is not available ",style='fail')
            return False
    except ValueError as err:
        return False
    
    

