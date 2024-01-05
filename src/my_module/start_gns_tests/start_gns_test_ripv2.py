"""Данный файл запускает проверочные тесты протокола RIPv2 на BM10."""

import pytest
import sys
import os
import yaml
import time


# !!! PATH fo import with position 1!!!
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# pprint.pprint(sys.path)
from cfg_bm10 import Cfg_bm10
from base_gns3 import Base_gns
from constants import (
    DEVICE_BM10,
    RESET_CONFIG_COMMAND,
    console,
)

console.print(
    "Тест работает по ПМИ 'Проверка поддержки RIPv2'.",
    "\nРекомендуется ознакомиться с описанием теста.",
    "\nВ ходе теста настройки устойства будут сброшены,",
    "\nбудет запрошено название лабы gns3 и предложены варианты ответа",
    style='info'
              )
time.sleep(5)
current_lab = Base_gns()  # test wait this lab - SSV_auto_BM10_RIPv2
print(current_lab.start_nodes_from_project())

r1 = Cfg_bm10(**DEVICE_BM10)

console.print("Стартует сброс конфига DUT перед настройкой под тест\n",
              style='info')
time.sleep(5)
# Сброс конфига
print(r1.cfg_reset(DEVICE_BM10, RESET_CONFIG_COMMAND))

console.print("Стартует настройка DUT под тест 'Проверка поддержки RIPv2'\n",
              style='info')
time.sleep(5)
# команды настройки конфига ripv2
with open("../command_cfg/commands_cfg_ripv2.yaml") as f15:
    commands_cfg_ripv2 = yaml.safe_load(f15)
r1 = Cfg_bm10(**DEVICE_BM10)
print(r1.cfg_base(DEVICE_BM10, commands_cfg_ripv2))

console.print(
    "Стартует настройка pytests под тест 'Проверка базового функционала RIPv2'\n",
    style='info'
    )
pytest.main(
    ["-v", "--tb=no",
     "--html=BULAT_TEST_BM10_RIPv2.html",
     "../tests_all/test_check_ripv2.py"]
     )
