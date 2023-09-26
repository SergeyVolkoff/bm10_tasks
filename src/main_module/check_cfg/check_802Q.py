import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from main_module.base_bm10 import Base_bm10


def check_vln_cfg(comm):

    """Из конфига вланов проверяем наличие вланов 2 и 3"""

    with open ("command_cfg/value_bm10.yaml") as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 =Base_bm10(**device)
    try:
        temp = r1.send_command(device,comm)
        if "bridge-vlan[1].ports='lan2'" in temp:
            return True

        if "bridge-vlan[2].ports='lan3'" in temp:
            return True
        else:
            return False
    except ValueError as err:
        return False
    

if __name__ == "__main__":
     result = check_vln_cfg("uci show network")
     print(result)