"""Проверка поддержки Multihoming 3G/4G failover (mwan3)."""


import pprint
import yaml
import pytest
import sys
import os
import time

sys.path.insert(1, os.path.join(sys.path[0],'..'))  # !!! PATH fo import with position 1!!!
# sys.path.insert(1, os.path.join(sys.path[0],'../command_cfg/'))  # !!! PATH fo import with position 1!!!
# sys.path.append(os.path.join(os.getcwd(),'..'))     # !!! PATH fo import!!!

# pprint.pprint(sys.path)
from ping3 import ping, verbose_ping
from cfg_bm10 import Cfg_bm10
from base_gns3 import Base_gns
from base_bm10 import Base_bm10
from constants import (
    DEVICE_BM10,
    RESET_CONFIG_COMMAND,
    CONSOLE,
)


CONSOLE.print(
    "Тест работает по ПМИ 'Проверка поддержки Multihoming 3G/4G failover (mwan3)'.",
    "\nРекомендуется ознакомиться с описанием теста.",
    "\nВ ходе теста настройки устойства будут сброшены,",
    "\nбудет запрошено название лабы gns3 и предложены варианты ответа",
    style='info'
              )
time.sleep(5)
current_lab = Base_gns() # test wait this lab - SSV_auto_BM10_wan_lte
CONSOLE.print("Стартует настройка лабы в gns3",style='info')
time.sleep(5)
print(current_lab.start_nodes_from_project())

r1 = Cfg_bm10(**DEVICE_BM10)

CONSOLE.print(
        "Стартует сброс конфига DUT перед настройкой под тест\n",
        style='info'
        )
time.sleep(5)
print(r1.cfg_reset(DEVICE_BM10, RESET_CONFIG_COMMAND))  # Сброс конфига 

CONSOLE.print(
        "Стартует настройка DUT под тест 'Проверка поддержки Multihoming 3G/4G failover (mwan3)'\n",
        style='info'
        )
time.sleep(5)
with open("../command_cfg/commands_cfg_wan_lte.yaml") as f15:
        commands_cfg_wan_lte = yaml.safe_load(f15)
r1 = Cfg_bm10(**DEVICE_BM10)
# Настройка DUT под тесt 
print(r1.cfg_base(DEVICE_BM10,commands_cfg_wan_lte))    

CONSOLE.print(
        "Стартует настройка pytests под тест 'Проверка поддержки Multihoming 3G/4G failover (mwan3)'\n",
        style='info'
        )
time.sleep(10)
pytest.main(
        ["-v",
         "--html=BULAT_TEST_BM10_Multihoming_failover.html",
         "../tests_all/test_check_multihom_failover.py"]
         )
