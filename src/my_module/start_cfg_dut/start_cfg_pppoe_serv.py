import sys
import os
import yaml
sys.path.insert(1, os.path.join(sys.path[0],'..'))

from cfg_bm10 import Cfg_bm10,SCP_cfg_ppoe

if __name__ == "__main__":
    with open("../command_cfg/value_bm10.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r2 = SCP_cfg_ppoe()
            print(r2.cfg_pppoe_serv())

        for t in temp:
            device = dict(t)
            r2 = SCP_cfg_ppoe()
            print(r2.cfg_pppoe_chap())

        for t in temp:
            device = dict(t)
            r2 = SCP_cfg_ppoe()
            print(r2.cfg_pppoe_opt())
            
        for t in temp:
            device = dict(t)
            r1 = Cfg_bm10(**device)
            with open("../command_cfg/commands_pppoe_server_cfg.yaml") as f14:         # команды настройки РРРРоЕ-server
                commands_pppoe_server_cfg = yaml.safe_load(f14)
            print(r1.cfg_pppoe_4(device,commands_pppoe_server_cfg))