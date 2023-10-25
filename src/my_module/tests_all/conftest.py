
import yaml
import pytest
import sys
import os
import time
sys.path.insert(1, os.path.join(sys.path[0],'..'))
sys.path.append(r"/home/ssw/Documents/bm10_tasks/src/my_module/") # !!! PATH fo import!!!


from ping3 import ping, verbose_ping
from base_gns3 import Base_gns
from gns3fy import Gns3Connector, Project, Node, Link
from cfg_bm10 import *
from base_bm10 import *



@pytest.fixture
def init_cfg_ripv2():
    with open("/home/ssw/Documents/bm10_tasks/src/my_module/command_cfg/value_bm10.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Cfg_bm10(**device)
            r1.cfg_ripv2(device,r1.commands_cfg_ripv2)
            time.sleep(5)

@pytest.fixture
def init_lab_gns():
    current_lab = Base_gns()
    current_lab.start_nodes_from_project()

@pytest.fixture
def wait_reboot():
        result=ping('192.168.1.1')
        while result is None:
            result=ping('192.168.1.1')
            print(result)
            print("DUT is rebooting, wait")
            time.sleep(5)
        else:
            print("DUT up after reboot, wait all protocols!")
            time.sleep(15)
            print( "all up!")


