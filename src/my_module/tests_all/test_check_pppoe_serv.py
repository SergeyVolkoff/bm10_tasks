from ipaddress import ip_interface
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
from check_all.check_pppoe_serv import check_ip_pppoe_neib

def test_check_int_pppoe_server():
    assert check_int_pppoe ("uci show network.test_pppoe_serv")==True, "No PPPoE on lan4-interface!!!"

"""
В блоке ниже используется параметризация mark.parametrize
"""
temp = r1.send_command(device,"ip r")
ip_peer = re.search(r'(?P<ip_peer>\d+.\d+.\d+.\d+) dev ppp0 proto',temp)
ip_peer=ip_peer.group('ip_peer')
ip_for_check = (
    ('192.168.1.1'),
    (ip_peer),
)
task_ids = ['ip_test({})'.format(t)
             # определям параметр ids чтобы сделать идентификаторы для понимания вывода теста
            for t in ip_for_check
            ]
@pytest.mark.parametrize("ip_test",ip_for_check,ids=task_ids)
            #("ip_test",ip_for_check,ids=task_ids)
            # используем параметризацию,
            # передаем в нее первый аргумент parametrize() — это строка с разделенным
            # запятыми списком имен — "ip_test" в нашем случае,
            # переменную указывающую на данные для проверки (ip_for_check) и ids

def test_check_ping_interface(ip_test,):
    assert check_ping_interf(ip_for_ping=f"{ip_test}")==True, f"*** IP {ip_test} unavaileble now ***"


def test_check_ip_pppoe_neib():
    assert check_ip_pppoe_neib('ip r')==True, "interface exist, but dont have ip, tunnel state DOWN"



