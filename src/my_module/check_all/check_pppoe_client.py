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
from constants import (
    DEVICE_BM10,
    RESET_CONFIG_COMMAND,
    CONSOLE,
)

r1 = Cfg_bm10(**DEVICE_BM10)

def check_int_pppoe_cl(comm): 
    
    CONSOLE.print("Test 1 \nОпределяем наличие настроенного интерфейса wan с РРРоЕ (есть ли конфиг вообще)",style='info')
    try:
        temp = r1.send_command(DEVICE_BM10, comm)
        if "pppoe" in temp:
            return True
        else:
            return False
    except ValueError as err:
        return False
    
def check_ip_pppoe(comm): 
    CONSOLE.print("Test 2 \nОпределяем наличие ip на интерфейсе wan с РРРоЕ",style='info')
    try:
        result_command = r1.send_command(DEVICE_BM10, comm)
        val_ppp_interface = re.search(r'\s+inet (?P<intf>\d+.\d+.\d+.\d+) peer (.{0,})pppoe-wan',result_command)
        ip_ppp = re.search(r'\s+inet (?P<ip_int>\d+.\d+.\d+.\d+) peer (?P<ip_peer>\d+.\d+.\d+.\d+).{0,}pppoe-wan', result_command)
        #ip_per=output.group('ip_peer')
        if val_ppp_interface is None:
            return False
        val_ppp_ip_group = val_ppp_interface.group()
        if "inet" in val_ppp_ip_group:
            print('Tunnel ok, ip client:',ip_ppp.group('ip_int'),', ip peer(serv):',ip_ppp.group('ip_peer'))
            return True
        else:
            if "state DOWN"in val_ppp_ip_group:
                print("interface exist, but state DOWN")
                return False
    except ValueError as err:
        return False

def check_ping_inet(): # check ping Internet
    CONSOLE.print("Test 3 \n Определяем доступность инета (8.8.8.8), в тестах эта проверка отключена")
    try:
        res_ping_inet = r1.ping_inet(DEVICE_BM10)
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
    CONSOLE.print("Test 4 \nПроверка доступности интерфейсов, исп-ся в тесте с параметрами",style='info')
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
    
    

if __name__=="__main__":
    print(check_ip_pppoe('ip a'))
