from base_bm10 import *
from cfg_bm10 import *

if __name__ == "__main__":
    with open("command_cfg/value_bm10.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Cfg_bm10(**device)
            r2 = SCP_cfg_ppoe()
            print(r2.cfg_pppoe_opt())
