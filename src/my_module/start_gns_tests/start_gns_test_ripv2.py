import pprint
import yaml
import pytest
import time
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0],'..'))  # !!! PATH fo import with position 1!!!
# sys.path.insert(1, os.path.join(sys.path[0],'../command_cfg/'))  # !!! PATH fo import with position 1!!!
# sys.path.append(os.path.join(os.getcwd(),'..'))     # !!! PATH fo import!!!

pprint.pprint(sys.path)

from ping3 import ping, verbose_ping
from cfg_bm10 import Cfg_bm10
from base_gns3 import Base_gns
from base_bm10 import Base_bm10


current_lab = Base_gns() # test wait this lab - SSV_auto_BM10_RIPv2
print(current_lab.start_nodes_from_project())

with open("../command_cfg/value_bm10.yaml")as f:
    temp = yaml.safe_load(f)
    for t in temp:
        device = dict(t)
        r1 = Cfg_bm10(**device)
        with open("../command_cfg/commands_cfg_ripv2.yaml") as f15:                # команды настройки Ripv2
                commands = yaml.safe_load(f15)
        print(r1.cfg_ripv2(device,commands))

        time.sleep(5)
        result=ping('192.168.1.1')
        while result is None:
            result=ping('192.168.1.1')
            print("DUT is rebooting, wait")
            time.sleep(5)
        else:
            print("DUT up after reboot, wait all protocols!")
            time.sleep(25)
            print( "All up!")

pytest.main(["-v","--tb=no","/home/ssw/Documents/bm10_tasks/src/my_module/tests_all/test_check_ripv2.py"])
