import yaml
import pytest
import sys
import os
import time
sys.path.insert(1, os.path.join(sys.path[0],'..'))
sys.path.append(r"/home/ssw/Documents/bm10_tasks/src/my_module/") # !!! PATH fo import!!!
# pprint.pprint(sys.path)

from ping3 import ping, verbose_ping
from cfg_bm10 import Cfg_bm10
from base_gns3 import Base_gns



current_lab = Base_gns()
print(current_lab.start_nodes_from_project())

with open("/home/ssw/Documents/bm10_tasks/src/my_module/command_cfg/value_bm10.yaml")as f:
    temp = yaml.safe_load(f)
    print(temp)
    for t in temp:
        device = dict(t)
        r1 = Cfg_bm10(**device)
        print(r1.cfg_ripv2(device,r1.commands_cfg_ripv2))
        time.sleep(5)

        result=ping('192.168.1.1')
        while result is None:
            result=ping('192.168.1.1')
            print("DUT is rebooting, wait")
            time.sleep(5)
        else:
            print("DUT up after reboot, wait all protocols!")
            time.sleep(1)
            print( "All up!")

pytest.main(["-v","--tb=no","/home/ssw/Documents/bm10_tasks/src/my_module/tests_all/test_check_ripv2.py"])