import yaml
import pytest
import time
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0],'..'))  # !!! PATH fo import with position 1!!!
from base_bm10 import Base_bm10
from cfg_bm10 import Cfg_bm10,SCP_cfg_ppoe
from base_gns3 import Base_gns

from rich import print

with open("../command_cfg/value_bm10.yaml")as f:
    temp = yaml.safe_load(f)
    for t in temp:
        device = dict(t)
        r1 = Cfg_bm10(**device)
        # Base_bm10.console.print(
        #     "Тест работает по ПМИ 'Проверка поддержки PPPoE-client'.\n Рекомендуется ознакомиться с описанием теста.\n В ходе теста будет запрошено название лабы и предложены варианты ответа",
        #     style='info'
        #             )
