import re

import pytest
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

"""
В блоке ниже используется параметризация mark.parametrize
"""
ip_for_check = (
    ('192.168.1.1'),
    ('192.168.10.1'),
    ('192.168.10.2'),
    ('192.168.20.1'),
    ('192.168.20.2'),
    ('200.1.10.2'),
    ('200.1.20.2'),
    ('1.1.1.1'),
    ('2.2.2.2'),
    
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

def test_check_ping_inter(ip_test):
    assert check_ping_interf(ip_for_ping=f"{ip_test}")==True, f"*** IP {ip_test} unavaileble now ***"
    
from check_all.check_ospfv2 import (check_enable_ospfv2,
                          check_route_ospfv2_net,
                          check_ping_interf,
                         )

def test_check_enable_ospfv2():
    assert check_enable_ospfv2()==True, "OSPFv2 disable!"

def test_check_route_ospfv2_net(): 
    # ф-я check_route_ripng_net() в цикле переберет список маршрутов, если нужного нет - вернет false
    assert check_route_ospfv2_net()==True, "*** Some route to the network 192.. or 200.. is not available! ***"

