import pprint
import re
import time
import yaml
import sys
import os
from ping3 import ping


sys.path.insert(1, os.path.join(sys.path[0],'..'))  # !!! PATH fo import with position 1!!!
#pprint.pprint(sys.path)

from base_bm10 import Base_bm10

with open("../command_cfg/value_bm10.yaml") as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Base_bm10(**device)

def check_enable_mwan3():
    try:
        temp = r1.send_command(device, 'mwan3 status')
        if "interface wan is offline and tracking is down" in temp:
            print("MWAN3 status - disable!")
            return False
        else:
            print("MWAN3 status - enable!")
            return True
    except ValueError as err:
        return False

def check_trsrt_mwan_stop():
    comm_mwan_stop = r1.send_command(device, 'mwan3 stop')
    time.sleep(2)
    show_mwan_stts = r1.send_command(device, 'mwan3 status')
    if "interface wan is offline and tracking is down" in show_mwan_stts:
        rslt_trsrt = r1.tracert_ip(device, ip_tracert="1.1.1.1")
        if '192.168.10.2' in rslt_trsrt:
            print (f"hop with an address 192.168.10.2 and 192.168.20.2 in the tracert!!! - {rslt_trsrt}")
            return False
        else:
            print(f"Tracing ok and goes only through 192.168.20.2 {rslt_trsrt}")
            return True
    else:
        print("MWAN3 status - enable!")        

if __name__ == "__main__":
    
            result = check_trsrt_mwan_stop()
            print(result)