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
    "Тест работает по ПМИ 'Проверка mwan3'.\n Рекомендуется ознакомиться с текстом теста.\n В ходе теста будет дважды запрошено название лабы и предложены варианты ответа",
    style='info'
              )
time.sleep(6)
current_lab = Base_gns() # test wait this lab - SSV_auto_BM10_MWAN
console.print("Стартует настройка лабы в gns3, в ходе тестов будет дважды предложено выбрать шаблон из списка. Выбор чего то кроме 'SSV_auto_BM10_MWAN' приведет к краху теста",style='info')
time.sleep(5)
print(current_lab.start_nodes_from_project())
console.print("Стартует настройка DUT под тест mwan3\n" ,style='info')
time.sleep(5)
with open("../command_cfg/value_bm10.yaml")as f:
    temp = yaml.safe_load(f)
    for t in temp:
        device = dict(t)
        r1 = Cfg_bm10(**device)
        with open("../command_cfg/commands_cfg_mwan3.yaml") as f15:                # команды настройки mwan3
                command_cfg_mwan = yaml.safe_load(f15)
        print(r1.cfg_mwan3(device,command_cfg_mwan))

        time.sleep(5)
        result=ping('192.168.1.1')
        while result is None:
            result=ping('192.168.1.1')
            print("DUT is rebooting, wait")
            time.sleep(5)
        else:
            print("DUT up after reboot, wait all protocols!")
            time.sleep(15)
            print( "All up!")
console.print("Стартует настройка tests под тест mwan3\n" ,style='info')
time.sleep(5)
pytest.main(["-v","-s","../tests_all/test_check_mwan3.py"])
