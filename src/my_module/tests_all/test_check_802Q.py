import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from check_all.check_802Q import *
   

def test_802Q():
    assert check_vln_cfg("uci show network") ==True, "Interface vlan 2 or 3 not exist"
