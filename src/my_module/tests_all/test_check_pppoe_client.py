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
from check_all.check_pppoe_client import *

def test_check_int_pppoe_cl():
    assert check_int_pppoe_cl ("uci show network.wan.proto")==True, "No PPPoE on wan-interface!!!"

@pytest.mark.skip
def test_check_ping_inet():
    assert check_ping_inet()== True, "Inet(8.8.8.8)- not available. Wan-port bad?"

def test_check_ip_pppoe():
    assert check_ip_pppoe('ip a')==True, "interface exist, but dont have ip, tunnel state DOWN"

@pytest.mark.skip
def test_check_tracert():
    assert check_tracert_peer() ==True, 'Tracert does not pass through server_ppoe'

"""
В блоке 28-50 используется параметризация mark.parametrize
"""

value_to_check_ip = ( # заносим в переменную данные для проверки
    ('200.1.1.1'),
    ('200.1.1.2'),
    
)
task_ids = ['ip_test({})'.format(t)
             # определям параметр ids чтобы сделать идентификаторы для понимания вывода теста
            for t in value_to_check_ip
            ]
@pytest.mark.parametrize("ip_test",value_to_check_ip,ids=task_ids)
            #("task",value_to_check_ip, ids=task_ids)
            # используем параметризацию,
            # передаем в нее первый аргумент parametrize() — это строка с разделенным
            # запятыми списком имен — "ip_test" в нашем случае,
            # переменную указывающую на данные для проверки (value_to_check_ip) и ids

def test_check_ping_interface(ip_test,):
    assert check_ping_interface(ip_for_ping=f"{ip_test}")==True, f"*** IP {ip_test} unavaileble now ***"

