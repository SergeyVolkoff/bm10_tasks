import yaml
import pytest
import pytest_html
import sys
import os
import time
from gns3fy import Gns3Connector, Project, Node, Link
sys.path.insert(1, os.path.join(sys.path[0],'..'))  # !!! PATH fo import with position 1!!!


from ping3 import ping, verbose_ping
from base_gns3 import Base_gns
from gns3fy import *
from cfg_bm10 import *
from base_bm10 import *


@pytest.fixture
def shut_R2_mwan():
    server_url = "http://10.27.193.245:3080"
    connector = Gns3Connector(url=server_url)
    name_lab = 'SSV_auto_BM10_MWAN'
    lab = Project(name=name_lab , connector=connector)
    lab.get()
    lab.open() # open lab
    r2 = Node(
            project_id=lab.project_id, 
            name='R2',
            connector=connector
            ) # создаем экз-р устр-ва
    r2.get()
    r2.stop()
    console.print (f'\nNode {r2.name} {r2.status}',style='success')
    # print(lab.stop_node())
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


