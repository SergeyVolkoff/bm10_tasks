import sys
import os
sys.path.insert(1, os.path.join(sys.path[0],'..'))  # !!! PATH fo import with position 1!!!
import pytest
from check_all.check_chang_pass import *

"""
В блоке ниже используется параметризация mark.parametrize
"""
new_pass = (
    
    ('12345'),
    ('qwerty'),
    ('QWERTY'),
    ('qWeRtY123'),
    ('!@#$%^&'),
    (''),
    ('root'),
)
pass_ids = ['new_pass({})'.format(t)
             # определям параметр ids чтобы сделать идентификаторы для понимания вывода теста
            for t in new_pass
            ]
@pytest.mark.parametrize("new_pass",new_pass,ids=pass_ids)
            #("ip_test",ip_for_check,ids=task_ids)
            # используем параметризацию,
            # передаем в нее первый аргумент parametrize() — это строка с разделенным
            # запятыми списком имен — "ip_test" в нашем случае,
            # переменную указывающую на данные для проверки (ip_for_check) и ids
def test_check_chang_pass( new_pass):
    
    print(f"Test \nПроверка смены пароля доступа по ssh")
    assert cfg_pass_new(pass_for_test = f'{new_pass}')==True, f"*** PASS unavaileble now ***"
    