import sys
import os
sys.path.insert(1, os.path.join(sys.path[0],'..'))

from cfg_bm10 import *

if __name__ == "__main__":
    with open("/home/ssw/Documents/bm10_tasks/src/my_module/command_cfg/value_bm10.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Cfg_bm10(**device)
            r2 = SCP_cfg_ppoe()
            print(r2.cfg_pppoe_chap())
