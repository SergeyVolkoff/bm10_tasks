
import pytest
from check_all.check_chang_pass import check_chang_pass

"""
В блоке ниже используется параметризация mark.parametrize
"""
pass_for_check = (
    ('root1'),
    ('root2'),
    ('root3'),
)
pass_ids = ['pass_for_check({})'.format(t)
             # определям параметр ids чтобы сделать идентификаторы для понимания вывода теста
            for t in pass_for_check
            ]
@pytest.mark.parametrize("pass_for_check",pass_for_check,ids=pass_ids)
            #("ip_test",ip_for_check,ids=task_ids)
            # используем параметризацию,
            # передаем в нее первый аргумент parametrize() — это строка с разделенным
            # запятыми списком имен — "ip_test" в нашем случае,
            # переменную указывающую на данные для проверки (ip_for_check) и ids

def test_check_chang_pass(pass_for_check,):
    assert check_chang_pass()==True, f"*** PASS {pass_for_check} unavaileble now ***"
    