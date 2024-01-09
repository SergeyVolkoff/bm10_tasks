import yaml
import pytest
# import pytest_html
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
from constants import (
    DEVICE_BM10,
    RESET_CONFIG_COMMAND,
    CONSOLE,
)

@pytest.fixture
def shut_R2_mwan():
    server_url = "http://10.27.193.245:3080"
    connector = Gns3Connector(url=server_url)
    name_lab = 'SSV_auto_BM10_MWAN3'
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
    CONSOLE.print (f'\nNode {r2.name} {r2.status}',style='success')
    time.sleep(8)
    


@pytest.fixture
def shut_R1_mwan():
    server_url = "http://10.27.193.245:3080"
    connector = Gns3Connector(url=server_url)
    name_lab = 'SSV_auto_BM10_wan_lte'
    lab = Project(name=name_lab , connector=connector)
    lab.get()
    lab.open() # open lab
    r2 = Node(
            project_id=lab.project_id, 
            name='R1',
            connector=connector
            ) # создаем экз-р устр-ва
    r2.get()
    r2.stop()
    CONSOLE.print (f'\nNode {r2.name} {r2.status}.',style='success')
    # print(lab.stop_node())
    CONSOLE.print('Waiting for mwan3 to be rebuilt the route',style='success')
    time.sleep(60)


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

data_pass_tests = (
    ('root'),
    ('root1'),
    ('root2'),
    ('root3'),
    ('root'),
)

@pytest.fixture
def reconnect ():
        """ ФУНКЦИЯ подключения, без чтения из файла"""
        with open("../command_cfg/value_bm10.yaml") as f:
            temp = yaml.safe_load(f)
            for t in temp:
                device = dict(t)
                r2 = Cfg_bm10(**device)
                # self.check_connection(device)
                