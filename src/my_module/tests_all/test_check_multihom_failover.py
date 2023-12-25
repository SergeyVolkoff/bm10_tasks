"""Проверка поддержки Multihoming 3G/4G failover (mwan3)."""

import pytest
from check_all.check_wan_lte import *

def test_check_int3G():
    assert check_int3G()==True, (
        "No interface on router or interface exist, but d'nt have ip address"
    )

"""
В блоке ниже используется параметризация mark.parametrize
"""
ip_for_check = (
    ('192.168.1.1'),
    ('192.168.20.1'),
    ('192.168.20.2'),
    ('1.1.1.1'),
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

def test_check_ping_inter(ip_test,):
    assert check_ping_interf(ip_for_ping=f"{ip_test}")==True, f"*** IP {ip_test} unavaileble now ***"

def test_check_tracert_when_mwan3_stop():
    assert check_trsrt_when_mwan_stop()==True, "Hop with LTE address in the tracert, but should not be!"

def test_check_enable_mwan3():
    assert check_enable_mwan3() ==True, "MWAN3 status - disable!"

def test_check_tracert_when_mwan3_up():
    assert check_trsrt_when_mwan_up()== True, "Not all hop in tracertHop with LTE address in the tracert, but should not be!"

def test_check_trsrt_mwanUp_wanDown(shut_R1_mwan):
    assert check_trsrt_mwanUp_wanDown()==True, "WANb FAIL!"
