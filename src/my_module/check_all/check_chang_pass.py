
import sys
import os
import yaml
sys.path.insert(1, os.path.join(sys.path[0],'..'))  # !!! PATH fo import with position 1!!!
from cfg_bm10 import Cfg_bm10

with open("../command_cfg/value_bm10.yaml") as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r2 = Cfg_bm10(**device)
            

def check_chang_pass():
    try:
        res_chenging = r2.cfg_pass(device,commands='passwd')
        print(res_chenging)
        if "root@" in res_chenging:
            print("New pass OK")
            return True
        else:
            print("Bad pass ")
            return False
    except ValueError as err:
        return False
    
if __name__ == "__main__":
    result = check_chang_pass()
    print(result)