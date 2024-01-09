import yaml
import pytest
import time
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0],'..'))  # !!! PATH fo import with position 1!!!
from cfg_bm10 import Cfg_bm10, SCP_cfg_ppoe
from base_gns3 import Base_gns
from base_bm10 import Base_bm10
from constants import (
    DEVICE_BM10,
    RESET_CONFIG_COMMAND,
    CONSOLE,
)

CONSOLE.print(
    "Тест работает по ПМИ 'Проверка поддержки PPPoE-server'.",
    "\nРекомендуется ознакомиться с описанием теста.",
    "\nВ ходе теста настройки устойства будут сброшены,",
    "\nбудет запрошено название лабы gns3 и предложены варианты ответа",
    style='info'
              )
time.sleep(5)
current_lab = Base_gns() # test wait this lab - SSV_auto_BM10_PPPoE
CONSOLE.print("Стартует настройка лабы в gns3",style='info')
time.sleep(5)
print(current_lab.start_nodes_from_project())

r1 = Cfg_bm10(**DEVICE_BM10)

CONSOLE.print("Стартует сброс конфига DUT перед настройкой под тест\n",
              style='info')
time.sleep(5)
# Сброс конфига
print(r1.cfg_reset(DEVICE_BM10, RESET_CONFIG_COMMAND)) 
        
CONSOLE.print("Стартует настройка DUT под тест 'Проверка поддержки PPPoE-server'\n" ,style='info')
time.sleep(5)
with open("../command_cfg/value_bm10.yaml")as f:
    temp = yaml.safe_load(f)
    for t in temp:
        device = dict(t)
        r2 = SCP_cfg_ppoe()
        print(r2.cfg_pppoe_serv())

    for t in temp:
        device = dict(t)
        r2 = SCP_cfg_ppoe()
        print(r2.cfg_pppoe_chap())

    for t in temp:
        device = dict(t)
        r2 = SCP_cfg_ppoe()
        print(r2.cfg_pppoe_opt())

r1 = Cfg_bm10(**DEVICE_BM10)
# команды настройки РРРРоЕ-server
with open("../command_cfg/commands_pppoe_server_cfg.yaml") as f14:
    commands_pppoe_server_cfg = yaml.safe_load(f14)
# Настройка DUT под тесt 
print(r1.cfg_base(DEVICE_BM10, commands_pppoe_server_cfg))# Настройка DUT под тесt 

CONSOLE.print(
    "Стартует настройка pytests под тест 'Проверка поддержки PPPoE-server'\n",
    style='info')
time.sleep(10)
pytest.main(
    ["-v",
     "--html=BULAT_TEST_BM10_PPPoE-server.html",
     "../tests_all/test_check_pppoe_serv.py"])

