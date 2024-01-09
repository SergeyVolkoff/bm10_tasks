"""Запускающий файл для тестирования PPPoE-client."""

import yaml
import pytest
import sys
import os
import time
sys.path.insert(1, os.path.join(sys.path[0],'..'))  # !!! PATH fo import with position 1!!!

from base_bm10 import Base_bm10
from cfg_bm10 import Cfg_bm10
from base_gns3 import Base_gns
from constants import (
    DEVICE_BM10,
    RESET_CONFIG_COMMAND,
    CONSOLE,
)


CONSOLE.print(
    "Тест работает по ПМИ 'Проверка поддержки PPPoE-client'.",
    "\nРекомендуется ознакомиться с описанием теста.",
    "\nВ ходе теста настройки устойства будут сброшены,",
    "\nбудет запрошено название лабы gns3 и предложены варианты ответа",
    style='info'
              )
time.sleep(5)
current_lab = Base_gns() # test wait this lab - SSV_auto_BM10_PPPoE-client
CONSOLE.print("Стартует настройка лабы в gns3",style='info')
time.sleep(5)
print(current_lab.start_nodes_from_project())

r1 = Cfg_bm10(**DEVICE_BM10)

CONSOLE.print("Стартует сброс конфига DUT перед настройкой под тест\n",
              style='info')
time.sleep(5)
# Сброс конфига
print(r1.cfg_reset(DEVICE_BM10, RESET_CONFIG_COMMAND))

CONSOLE.print("Стартует настройка DUT под тест 'Проверка поддержки PPPoE-client'\n",
              style='info')
time.sleep(5)
# команды настройки
with open("../command_cfg/commands_pppoe_client_cfg.yaml") as f15: # команды настройки 
    commands_cfg_pppoe_client = yaml.safe_load(f15)
r1 = Cfg_bm10(**DEVICE_BM10)
print(r1.cfg_base(DEVICE_BM10,commands_cfg_pppoe_client))    # Настройка DUT под тесt 

CONSOLE.print(
    "Стартует настройка pytests под тест 'Проверка поддержки PPPoE-client'\n",
    style='info')
time.sleep(10)
pytest.main(
    ["-v",
     "--html=BULAT_TEST_BM10_PPPoE-client.html",
     "../tests_all/test_check_pppoe_client.py"])

