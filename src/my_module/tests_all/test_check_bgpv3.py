import re

import pytest
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from check_all.check_bgpv3 import *



def test_check_enable_bgpv3():
    assert check_enable_bgpv3()==True, "BGP disable"


def test_check_redistr_kernel():
    assert check_redistr_kernel()==True, "Redistribute_kernel - disable"


def test_check_redistr_connected():
    assert check_redistr_connected()==True, "Redistribute_connected - disable"


def test_check_redistr_static():
    assert check_redistr_static()==True, "Redistribute_static - disable"


def test_check_route10_bgpv3():
    assert check_route10_bgpv3()==True, "*** Route to the network 200.1.10.0/24 is not available! ***"


def test_check_route20_bgpv3():
    assert check_route20_bgpv3()==True, "*** Route to the network 200.1.20.0/24 is not available! ***"


"""
В блоке ниже используется параметризация mark.parametrize
"""
ip_for_check = (
    ('200.1.10.1'),
    ('200.1.20.1'),
    
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

def test_check_ping_loopback_neighbor(ip_test):
    assert check_ping_interf(ip_for_ping=f"{ip_test}")==True, f"*** IP {ip_test} unavaileble now***"

def test_check_redistr_static_routeDut_toR2():
    pass