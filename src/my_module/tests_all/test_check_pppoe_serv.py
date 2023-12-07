import re

import pytest
# import tasks
# from tasks import Task
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from check_all.check_pppoe_serv import *

def test_check_int_pppoe_server():
    assert check_int_pppoe ("uci show network.test_pppoe_serv")==True, "No PPPoE on lan4-interface!!!"

def test_check_ip_pppoe_neib():
    assert check_ip_pppoe_neib('ip r')==True, "interface exist, but dont have ip, tunnel state DOWN"



