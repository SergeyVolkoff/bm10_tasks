
import yaml
import pytest

from base_gns3 import Base_gns
from gns3fy import Gns3Connector, Project, Node, Link
from cfg_bm10 import *
from base_bm10 import *

@pytest.fixture
def init_lab_gns():
    current_lab = Base_gns()
    current_lab.start_nodes_from_project()


@pytest.fixture
def init_cfg_ripv2():
    with open("command_cfg/value_bm10.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Cfg_bm10(**device)
            r1.cfg_ripv2(device,r1.commands_cfg_ripv2)
