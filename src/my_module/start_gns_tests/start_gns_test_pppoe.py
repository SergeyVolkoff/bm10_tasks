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
    "Тест работает по ПМИ 'Проверка поддержки PPPoE-server'.\n Рекомендуется ознакомиться с описанием теста.\n В ходе теста будет запрошено название лабы и предложены варианты ответа",
    style='info'
              )
time.sleep(6)
current_lab = Base_gns() # test wait this lab - SSV_auto_BM10_PPPoE
CONSOLE.print("Стартует настройка лабы в gns3",style='info')
time.sleep(5)
print(current_lab.start_nodes_from_project())
CONSOLE.print("Стартует сброс конфига DUT перед настройкой под тест\n" ,style='info')
time.sleep(5)
with open("../command_cfg/value_bm10.yaml")as f:
    temp = yaml.safe_load(f)
    for t in temp:
        device = dict(t)
        r1 = Cfg_bm10(**device)
        with open("../command_cfg/commands_reset_cfg.yaml") as f14:  # команды сброса конфига
                commands_reset_cfg = yaml.safe_load(f14)
        print(r1.cfg_reset(device,commands_reset_cfg))  # Сброс конфига 
        
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
                
            for t in temp:
                device = dict(t)
                r1 = Cfg_bm10(**device)
                with open("../command_cfg/commands_pppoe_server_cfg.yaml") as f14:         # команды настройки РРРРоЕ-server
                    commands_pppoe_server_cfg = yaml.safe_load(f14)
                print(r1.cfg_base(device,commands_pppoe_server_cfg))    # Настройка DUT под тесt 

CONSOLE.print("Стартует настройка pytests под тест 'Проверка поддержки PPPoE-server'\n" ,style='info')
time.sleep(10)
pytest.main(["-v","--html=BULAT_TEST_BM10_PPPoE-server.html","../tests_all/test_check_pppoe_serv.py"])

