import sys
import os
import yaml
sys.path.insert(1, os.path.join(sys.path[0],'..'))
from cfg_bm10 import Cfg_bm10

if __name__ == "__main__":
    with open("../command_cfg/value_bm10.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Cfg_bm10(**device)
            with open("../command_cfg/commands_cfg_mwan3.yaml") as f15:  # команды настройки mwan3
                commands_cfg_mwan3 = yaml.safe_load(f15)
            print(r1.cfg_ripv2(device,commands_cfg_mwan3))

