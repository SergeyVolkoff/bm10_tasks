import yaml
import pytest

from base_gns3 import Base_gns
from cfg_bm10 import *
from base_bm10 import *
from test_check_ripv2 import *

if __name__=="__main__":
    
    current_lab = Base_gns()
    print(current_lab.start_nodes_from_project())
    with open("command_cfg/value_bm10.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Cfg_bm10(**device)
            print(r1.cfg_ripv2(device,r1.commands_cfg_ripv2))
