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

def check_int3G():
    console.print("Test 0 \nПроверка интерфейса 3G",style='info')

    temp = r1.send_command(device,"uci show network | grep wanb")
    result = ""
    for line in temp:
        if "wanb.device" in temp:
            name_intf = re.search(r'network.(\S+).device', temp).group() # type: ignore
            result += name_intf
            temp = r1.send_command(device,"ifconfig |grep -A 1 wwan0")
            if "addr:" in temp:
                ip_int = re.search(r'inet addr:(\S+)', temp).group() # type: ignore
                result +=  ip_int
                console.print(result,style='success')
                return True
            else:
                result = name_intf
                console.print("*" * 30)
                console.print(name_intf, "interface exist, but d'nt have ip addr",style='fail')
                return False
            break
        else:
            result = "No interface on router"
            console.print(result,style='fail')
            return False
    return result


def check_ping_interf(ip_for_ping): # check ping Internet

    console.print("Test 1 \nПроверка доступности интерфейсов соседей, исп-ся в тесте с параметрами",style='info')

    try:
        res_ping_inet = r1.ping_ip(device,ip_for_ping)
        print(res_ping_inet)
        if "destination available" in res_ping_inet:
            console.print("Interface availeble ",style="success")
            return True
        else:
            console.print("Interface is not available ",style='fail')
            return False
    except ValueError as err:
        return False
    
def check_trsrt_when_mwan_stop():

    console.print("Test 5 \nПроверка, что при выкл mwan3 трассерт проходит только через wan согласно метрике шлюза",style='info')
    
    comm_mwan_stop = r1.send_command(device, 'mwan3 stop')
    time.sleep(2)
    show_mwan_stts = r1.send_command(device, 'mwan3 status')
    if "interface wan is offline and tracking is down" in show_mwan_stts:
        rslt_trsrt = r1.tracert_ip(device, ip_tracert="1.1.1.1")
        if '192.168.20.2'  not in rslt_trsrt:
            console.print (f"\nHop with LTE address in the tracert, but should not be! -\n  {rslt_trsrt}",style='fail')
            return False
        else:
            if "can't connect to remote host" in rslt_trsrt:
                print(rslt_trsrt)
                return False
            else:
                console.print(f"\nTracing ok and goes only through 192.168.20.2 \n {rslt_trsrt}",style="fail")
                return True
    else:
        print("\nMWAN3 status - enable!\n ")  

def check_enable_mwan3():

    console.print("Test 5 \nПроверка, что mwan3 включен на обоих интерфейсах",style='info')
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
    

def check_trsrt_when_mwan_up():

    console.print("Test6 \nПроверка, что при вкл mwan3 трассерт идет через wan!",style='info')
    
    r1.send_command(device, '/sbin/ifup wan')
    r1.send_command(device, '/sbin/ifup wanb')
    time.sleep(8)
    show_mwan_stts = r1.send_command(device, 'mwan3 status')
    if "interface wan is online" and "wanb is online"  in show_mwan_stts:
        rslt_trsrt = r1.tracert_ip(device, ip_tracert="1.1.1.1")
        if '192.168.20.2'  not in rslt_trsrt:
            console.print (f"\nHop with LTE address in the tracert, but should not be!!! -\n  {rslt_trsrt}",style='fail')
            return False
        else:
            if "can't connect to remote host" in rslt_trsrt:
                print(rslt_trsrt)
                return False
            else:
                console.print(f"\nTracing ok and goes only through 192.168.20.2 \n {rslt_trsrt}",style="fail")
                return True
    else:
        print("\nMWAN3 status - disable!\n ")

def check_trsrt_mwanUp_wanDown(): # ДОПИСАТЬ!!!
    console.print(
        "Test 7 \nПроверка, что при вкл mwan3 и выкл линке на r2 трасса пройдет через LTE",
        style='info'
        )
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

# if __name__ =="__main__":
#     result = check_int3G()
#     print (result)