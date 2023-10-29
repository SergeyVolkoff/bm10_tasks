import sys
import os
sys.path.insert(1, os.path.join(sys.path[0],'..'))
from cfg_bm10 import *


if __name__ == "__main__":
    with open("../command_cfg/value_bm10.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Cfg_bm10(**device)
            with open ("../command_cfg/commands_802_1d_cfg.yaml") as f4:           # команды настройки STP+ базовые настройки
                commands_template = yaml.safe_load(f4)
            print(r1.cfg_base_802(device, commands_template))
