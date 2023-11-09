import pprint
import re
import time
from py import test
import yaml
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0],'..'))  # !!! PATH fo import with position 1!!!
# pprint.pprint(sys.path)

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


with open("../command_cfg/value_bm10.yaml") as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Base_bm10(**device)


def check_enable_mwan3():

    # Проверка, что mwan3 включен на обоих интерфейсах
    
    r1.send_command(device, 'mwan3 start')
    try:
        temp = r1.send_command(device, 'mwan3 status')
        if "wan is online" and "wanb is online" in temp:
            console.print("\nMWAN3 status - enable! \n ",style="success")
            return True
        else:
            console.print("\nMWAN3 status - disable! \n ",style='fail')
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
            console.print (f"\nHop with an address 192.168.10.2 in the tracert, but should not be!!! -\n  {rslt_trsrt}",style='fail')
            return False
        else:
            if "can't connect to remote host" in rslt_trsrt:
                print(rslt_trsrt)
                return False
            else:
                console.print(f"\nTracing ok and goes only through 192.168.20.2 \n {rslt_trsrt}",style="success")
                return True
    else:
        print("\nMWAN3 status - enable!\n ")      


def check_trsrt_when_mwan_up():

    # Проверка, что при вкл mwan3 трассерт балансируется через оба шлюза!
    
    r1.send_command(device, '/sbin/ifup wan')
    #r1.send_command(device, '/sbin/ifup wanb')
    time.sleep(7)
    show_mwan_stts = r1.send_command(device, 'mwan3 status')
    temp1=r1.tracert_ip(device, ip_tracert="1.1.1.1")
    temp1 = re.search(r' 1  (?P<ip_peer>\S+)',temp1)
    rslt_trsrt1 = temp1.group('ip_peer')
    temp2 = r1.tracert_ip(device,ip_tracert="2.2.2.2")
    temp2 = re.search(r' 1  (?P<ip_peer>\S+)',temp2)
    rslt_trsrt2 = temp2.group('ip_peer')
    if rslt_trsrt2 and rslt_trsrt1:
        if  rslt_trsrt1 != rslt_trsrt2:
            console.print (f"\nHops with an address 192.168.10.2 and 192.168.20.2 in the tracert -\ntraffic balanced!!! : \nFor trasert 1 first hop is {rslt_trsrt1}\nFor trasert 2 first hop is {rslt_trsrt2}\n"    
                ,style="success"
                            )
            return True
        else:
            console.print(f'\nNot all hop in tracert -\n  {rslt_trsrt1} \n {rslt_trsrt2}',style='fail',)
            return False
    else:
        print("\nMWAN3 status - disable! or tracert fail")
        return False

def check_ping_interf(ip_for_ping): # check ping Internet

    # Проверка доступности интерфейсов соседей, исп-ся в тесте с параметрами

    try:
        res_ping_inet = r1.ping_ip(device,ip_for_ping)
        print(res_ping_inet)
        if "destination available" in res_ping_inet:
            console.print("\nInterface availeble\n ",style="success")
            return True
        else:
            console.print("\nInterface is not available\n ",style='fail')
            return False
    except ValueError as err:
        return False


def check_tracert_when_mwan3_up_LinkR2disable():

    # Проверка, что при вкл mwan3 и выкл линке на r2 трасса пройдет через r1
    
    show_mwan_stts = r1.send_command(device, 'mwan3 status')
    if "192.168.10.0/24" in show_mwan_stts:
        rslt_trsrt = r1.tracert_ip(device, ip_tracert="1.1.1.1")
        if  '192.168.10.2'  in rslt_trsrt:
            console.print (f"\nProtection channel via interface wanb - OK, tracert - OK!!! - \n{rslt_trsrt}",style="success")
            return True
        else:
            console.print(f'\nWANb FAIL !!! - {rslt_trsrt}',style='fail')
            return False
    else:
        console.print("MWAN3 status - disable!",style='fail')

if __name__ == "__main__":
    
            result = check_trsrt_when_mwan_up()
            print(result)