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

def check_int_pppoe_cl(comm): 
     # Определяем наличие настроенного интерфейса ван с РРРоЕ (есть ли конфиг вообще)
    try:
        temp = r1.send_command(device, comm)
        if "pppoe" in temp:
            return True
        else:
            return False
    except ValueError as err:
        return False
    
def check_ip_pppoe(comm): 
    # check ip for client and serv
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

def check_tracert_peer():
    try:
        result_tracert =  r1.tracert_ip(device) # add !!!!
        if ' Tracert passes through server-peer' in result_tracert:
            return True
        else:
            return False
    except ValueError as err:
        return False
'''
используется параметризация!!
'''
def check_ip_peer(comm): # возвращает ip сервера (ip_per) для теста test_check_ip_peer
    try:
        temp = r1.send_command(device,comm)
        output = re.search(r'\s+inet (?P<ip_int>\d+.\d+.\d+.\d+) peer (?P<ip_peer>\d+.\d+.\d+.\d+).{0,}pppoe-wan', temp)
        ip_per=output.group('ip_peer')
        return ip_per
    except ValueError as err:
        return False
    
    
if __name__ =="__main__":
    result = check_ip_peer("ip a")
    print (result)

