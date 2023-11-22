import pprint
import re
import sys
import os
import time
from py import test
import yaml


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


'''
Проверяем работу wifi моста поднятого с телефоном или роутером
'''

with open("../command_cfg/value_bm10.yaml") as f:
    temp = yaml.safe_load(f)
    for t in temp:
        device = dict(t)
        r1 = Base_bm10(**device)

def check_WiFi_AP(comm): 
    # Определяем наличие настроенного бриджа (есть ли конфиг вообще нужный интерфейс)
    try:
        temp = r1.send_command(device, comm)
        if "Br_AP" in temp:
            return True
        else:
            return False
    except ValueError as err:
        return False
    
def check_ping_inet():
    ip_for_ping = "8.8.8.8"
    try:
        res_ping_inet = r1.ping_inet(device)
        if "destination available" in res_ping_inet:
            print("Bridge OK")
        else:
            print("Bridge bad, inet(8.8.8.8)- not available")
    except ValueError as err:
        return False
    
def check_pingGW(): 
     # Пингуем шлюз-телефон
    output_rout = r1.send_command(device,"ip route")              # этой командой получаем основной маршрут
    print(output_rout)
    ip_route = re.search(r'default via (\S+)',output_rout).group(1)  # реджектим ip шлюза
    r1.ip_for_ping=ip_route                                          # переопределяем ip из основного класса R1
    try:
        res_pingGW = r1.ping_ip(device,r1.command_ping)           # проверяем доступность шлюза (
        if "destination  available " in res_pingGW:               #если отвечает, значит все ок, возвращаем тру
            print("GW available!")
            return True
        else:
            if " out of destination" in res_pingGW:            #если не отвечает - не правльно настроено, возвращаем фолс
                print("GW out")
                return False
    except ValueError as err:
        return False



if __name__ =="__main__":
    comm = 'uci show network.Br_AP'
    result = check_pingGW()
    print (result)
