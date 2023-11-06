import pprint
import re
import time
import yaml
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0],'..'))  # !!! PATH fo import with position 1!!!
#pprint.pprint(sys.path)

from ping3 import ping
from base_gns3 import Base_gns
from base_bm10 import Base_bm10
from gns3fy import *


with open("../command_cfg/value_bm10.yaml") as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Base_bm10(**device)

def check_enable_mwan3():

    # Проверка, что mwan3 включен на обоих интерфейсах
    
    try:
        temp = r1.send_command(device, 'mwan3 status')
        if "wan is online" and "wanb is online" in temp:
            print("MWAN3 status - enable!")
            return True
        else:
            print("MWAN3 status - disable !")
            return False
    except ValueError as err:
        return False

def check_trsrt_when_mwan_stop():

    # Проверка, что при выкл mwan3 трассерт проходит только через r2 согласно метрике шлюза
    
    comm_mwan_stop = r1.send_command(device, 'mwan3 stop')
    time.sleep(2)
    show_mwan_stts = r1.send_command(device, 'mwan3 status')
    if "interface wan is offline and tracking is down" in show_mwan_stts:
        rslt_trsrt = r1.tracert_ip(device, ip_tracert="1.1.1.1")
        if '192.168.10.2' in rslt_trsrt:
            print (f"hop with an address 192.168.10.2 and 192.168.20.2 in the tracert!!! - {rslt_trsrt}")
            return False
        else:
            if "can't connect to remote host" in rslt_trsrt:
                return rslt_trsrt
            else:
                print(f"Tracing ok and goes only through 192.168.20.2 {rslt_trsrt}")
                return True
    else:
        print("MWAN3 status - enable!")      


def check_trsrt_when_mwan_up():

    # Проверка, что при вкл mwan3 трассерт балансируется через оба шлюза!

    time.sleep(5)
    show_mwan_stts = r1.send_command(device, 'mwan3 status')
    if "192.168.20.0/24" in show_mwan_stts:
        rslt_trsrt = r1.tracert_ip(device, ip_tracert="1.1.1.1")
        if  '192.168.20.2' and '192.168.10.2'  in rslt_trsrt:
            print (f"Hop with an address 192.168.10.2 and 192.168.20.2 in the tracert - traffic balanced!!! - {rslt_trsrt}")
            return True
        else:
            print(f'Not all hop in tracert - {rslt_trsrt}')
            return False
    else:
         print("MWAN3 status - disable!")


def check_ping_interf(ip_for_ping): # check ping Internet

    # Проверка доступности интерфейсов соседей, исп-ся в тесте с параметрами

    try:
        res_ping_inet = r1.ping_ip(device,ip_for_ping)
        print(res_ping_inet)
        if "destination available" in res_ping_inet:
            print("Interface availeble")
            return True
        else:
            print("Interface is not available")
            return False
    except ValueError as err:
        return False




def shut_R2_mwan():
    current_lab = Base_gns()
    print(current_lab.start_node())

def check_tracert_when_mwan3_up_LinkR2disable():

    # Проверка, что при вкл mwan3 и выкл линке на r2 трасса пройдет через r1
    current_lab = Base_gns()
    print(current_lab.start_node())
    time.sleep(5)
    show_mwan_stts = r1.send_command(device, 'mwan3 status')
    if "192.168.10.0/24" in show_mwan_stts:
        rslt_trsrt = r1.tracert_ip(device, ip_tracert="1.1.1.1")
        if  '192.168.10.2'  in rslt_trsrt:
            print (f"tracert OK, wanb OK!!! - {rslt_trsrt}")
            return True
        else:
            print(f'WANb FAIL !!! - {rslt_trsrt}')
            return False
    else:
         print("MWAN3 status - disable!")

if __name__ == "__main__":
    
            result = check_tracert_when_mwan3_up_LinkR2disable()
            print(result)