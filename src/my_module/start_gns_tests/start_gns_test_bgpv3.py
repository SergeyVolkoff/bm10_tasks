import pprint
import yaml
import pytest
import time
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0],'..'))  # !!! PATH fo import with position 1!!!
# sys.path.insert(1, os.path.join(sys.path[0],'../command_cfg/'))  # !!! PATH fo import with position 1!!!
# sys.path.append(os.path.join(os.getcwd(),'..'))     # !!! PATH fo import!!!

# pprint.pprint(sys.path)

from ping3 import ping, verbose_ping
from cfg_bm10 import Cfg_bm10
from base_gns3 import Base_gns
from base_bm10 import Base_bm10

from rich import print
from rich.theme import Theme
from rich.console import Console
my_colors = Theme(
     {
        "success":" bold green",
        "fail": "bold red",
        "info": "bold blue"

    }
)
console = Console(theme=my_colors)

console.print(
    "Тест работает по ПМИ 'Проверка работы протокола BGP'.\n Рекомендуется ознакомиться с текстом теста.\n В ходе теста будет запрошено название лабы и предложены варианты ответа",
    style='info'
              )
time.sleep(6)
current_lab = Base_gns() # test wait this lab - SSV_auto_BM10_BGP
console.print("Стартует настройка лабы в gns3",style='info')
time.sleep(5)
print(current_lab.start_nodes_from_project())
console.print("Стартует сброс конфига DUT перед настройкой под тест\n" ,style='info')
time.sleep(5)
with open("../command_cfg/value_bm10.yaml")as f:
    temp = yaml.safe_load(f)
    for t in temp:
        device = dict(t)
        r1 = Cfg_bm10(**device)
        with open("../command_cfg/commands_reset_cfg.yaml") as f14:  # команды сброса конфига
                commands_reset_cfg = yaml.safe_load(f14)
        print(r1.cfg_bgpv3(device,commands_reset_cfg))  # Сброс конфига 
        console.print("Стартует настройка DUT под тест 'Проверка работы протокола BGP'\n" ,style='info')
        time.sleep(5)
        with open("../command_cfg/value_bm10.yaml")as f:
                temp = yaml.safe_load(f)
                for t in temp:
                    device = dict(t)
                    r1 = Cfg_bm10(**device)
                    with open("../command_cfg/commands_cfg_bgpv3.yaml") as f15: # команды настройки BGP
                            commands_cfg_bgpv3 = yaml.safe_load(f15)
                    print(r1.cfg_bgpv3(device,commands_cfg_bgpv3))    # Настройка DUT под тесt BGP
console.print("Стартует настройка pytests под тест 'Проверка работы протокола BGP'\n" ,style='info')
time.sleep(25)
pytest.main(["-v","--html=BULAT_TEST_BM10_BGP.html","../tests_all/test_check_bgpv3.py"])
