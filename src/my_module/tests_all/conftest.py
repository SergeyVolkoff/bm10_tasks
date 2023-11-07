
import yaml
import pytest
import sys
import os
import time
sys.path.insert(1, os.path.join(sys.path[0],'..'))  # !!! PATH fo import with position 1!!!


from ping3 import ping, verbose_ping
from base_gns3 import Base_gns
from gns3fy import *
from cfg_bm10 import *
from base_bm10 import *


@pytest.fixture
def shut_R2_mwan():
    current_lab = Base_gns()
    print(current_lab.stop_node())
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


