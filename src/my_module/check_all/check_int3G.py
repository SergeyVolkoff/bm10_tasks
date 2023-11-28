import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from base_bm10 import Base_bm10


with open("../command_cfg/value_bm10.yaml") as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Base_bm10(**device)

def check_int3G():
    print(" \nПроверка интерфейса 3G")

    temp = r1.send_command(device,"uci show network | grep wanb")
    result = ""
    for line in temp:
        if "wanb.device" in temp:
            name_intf = re.search(r'network.(\S+).device', temp).group()
            result += name_intf
            temp = r1.send_command(device,"ifconfig |grep -A 1 wwan0")
            if "addr:" in temp:
                ip_int = re.search(r'inet addr:(\S+)', temp).group()
                result +=  ip_int
                print(result)
                return True
            else:
                result = name_intf
                print("*" * 30)
                print(name_intf, "exist, but d'nt have ip addr")
                return False
            break
        else:
            result = "No interface on router"
            print(result)
            return False
    return result
    
if __name__ =="__main__":
    result = check_int3G("uci show network | grep wanb")
    print (result)
