import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from main_module.base_bm10 import Base_bm10
from check_cfg.check_802Q.py import check_vln_cfg
def test_802Q():
    assert check_vln_cfg("uci show network") ==True, "Interface vlan 2 or 3 not exist"
