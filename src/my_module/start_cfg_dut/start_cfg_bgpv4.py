import sys
import os
import yaml
sys.path.insert(1, os.path.join(sys.path[0],'..'))

from base_bm10 import Base_bm10
from cfg_bm10 import Cfg_bm10

if __name__ == "__main__":
    with open("../command_cfg/value_bm10.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Cfg_bm10(**device)
            with open("../command_cfg/commands_cfg_bgpv3.yaml") as f18:
                commands_template = yaml.safe_load(f18)
            print(r1.cfg_bgpv3(device,commands_template)) 