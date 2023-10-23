import yaml
import pytest

from base_gns3 import Base_gns
from cfg_bm10 import *
from base_bm10 import *

    
# current_lab = Base_gns()
# print(current_lab.start_nodes_from_project())

with open("command_cfg/value_bm10.yaml")as f:
    temp = yaml.safe_load(f)
    for t in temp:
        device = dict(t)
        r1 = Cfg_bm10(**device)
        #print(r1.cfg_ripv2(device,r1.commands_cfg_ripv2))
        time.sleep(5)

        result=ping('192.168.1.1')
        while result is None:
            result=ping('192.168.1.1')
            print("DUT is rebooting, wait")
            time.sleep(5)
        else:
            print("DUT up after reboot, wait all protocols!")
            time.sleep(15)
            print( "All up!")

from test_check_ripv2 import *
pytest.main(["--tb=no","-v","test_check_ripv2.py"])