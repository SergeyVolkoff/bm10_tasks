import yaml
import pytest
import time
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0],'..'))  # !!! PATH fo import with position 1!!!
from base_bm10 import Base_bm10
from cfg_bm10 import Cfg_bm10
from base_gns3 import Base_gns



Cfg_bm10.console.print(
    "Тест работает по ПМИ 'Проверка поддержки PPPoE-client'.\n Рекомендуется ознакомиться с описанием теста.\n В ходе теста будет запрошено название лабы и предложены варианты ответа",
    style='info'
              )
Cfg_bm10.SLEEP_TIME5
current_lab = Base_gns() # test wait this lab - SSV_auto_BM10_PPPoE-client
Cfg_bm10.console.print("Стартует настройка лабы в gns3",style='info')
Cfg_bm10.SLEEP_TIME5
print(current_lab.start_nodes_from_project())
Cfg_bm10.console.print("Стартует сброс конфига DUT перед настройкой под тест\n" ,style='info')
Cfg_bm10.SLEEP_TIME5
with open("../command_cfg/value_bm10.yaml")as f:
    temp = yaml.safe_load(f)
    for t in temp:
        device = dict(t)
        r1 = Cfg_bm10(**device)
        with open("../command_cfg/commands_reset_cfg.yaml") as f14:  # команды сброса конфига
                commands_reset_cfg = yaml.safe_load(f14)
        print(r1.cfg_reset(device,commands_reset_cfg))  # Сброс конфига 
        Cfg_bm10.SLEEP_TIME5
        Cfg_bm10.console.print("Стартует настройка DUT под тест 'Проверка поддержки PPPoE-client'\n" ,style='info')
        with open("../command_cfg/value_bm10.yaml")as f:
            temp = yaml.safe_load(f)
            for t in temp:
                device = dict(t)
                r1 = Cfg_bm10(**device)
                with open("../command_cfg/commands_pppoe_client_cfg.yaml") as f15: # команды настройки 
                        commands_cfg_pppoe_client = yaml.safe_load(f15)
                print(r1.cfg_base(device,commands_cfg_pppoe_client))    # Настройка DUT под тесt 

Cfg_bm10.console.print("Стартует настройка pytests под тест 'Проверка поддержки PPPoE-client'\n" ,style='info')
Cfg_bm10.SLEEP_TIME10 
# pytest.main(["-v","-s","--html=BULAT_TEST_BM10_PPPoE-client.html","../tests_all/test_check_pppoe_client.py"])

