
import yaml
import pytest
import time

from ping3 import ping, verbose_ping
from base_gns3 import Base_gns
from gns3fy import Gns3Connector, Project, Node, Link
from cfg_bm10 import *
from base_bm10 import *



@pytest.fixture
def init_cfg_ripv2():
    with open("command_cfg/value_bm10.yaml")as f:
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
            print("DUT in reboot, weit!")
            time.sleep(5)
        else:
            print("DUT up after reboot, weit all protocols!")
            time.sleep(5)
            return "all up!"

@pytest.fixture
def init_ssh_after_reboot():
     with open("command_cfg/value_bm10.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Cfg_bm10(**device)
            r1.check_connection(device)
