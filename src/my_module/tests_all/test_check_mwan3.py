import pytest
import pytest_html
from check_all.check_mwan3 import *


"""
В блоке ниже используется параметризация mark.parametrize
"""
ip_for_check = (
    ('192.168.1.1'),
    ('192.168.10.1'),
    ('192.168.10.2'),
    ('192.168.20.1'),
    ('192.168.20.2'),
    ('200.1.20.1'),
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

def test_check_ping_inter(ip_test,):
    assert check_ping_interf(ip_for_ping=f"{ip_test}")==True, f"*** IP {ip_test} недоступен в данный момент ***"


def test_check_tracert_when_mwan3_stop():
    assert check_trsrt_when_mwan_stop()==True, "Или недоступен удаленный хост или в трассерте есть оба плеча, чего не должно быть.См вывод трасерта."


def test_check_enable_mwan3():
    assert check_enable_mwan3() ==True, "MWAN3 status - disable!"


def test_check_tracert_when_mwan3_up():
    assert check_trsrt_when_mwan_up()== True, "Не все хопы в трассерте"


def test_check_tracert_when_mwan3_up_LinkR2disable(shut_R2_mwan):
    assert check_tracert_when_mwan3_up_LinkR2disable()==True, "WANb FAIL!"

