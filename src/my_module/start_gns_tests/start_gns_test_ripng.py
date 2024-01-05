"""Данный файл запускает проверочные тесты протокола RIPng на BM10."""

import pytest
import sys
import time
import os
import yaml
# !!! PATH fo import with position 1!!!
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# pprint.pprint(sys.path)
from ping3 import ping
from cfg_bm10 import Cfg_bm10
from base_gns3 import Base_gns
from constants import *

current_lab = Base_gns()  # test wait this lab - SSV_auto_BM10_RIPv2
print(current_lab.start_nodes_from_project())

r1 = Cfg_bm10(**DEVICE_BM10)
with open("../command_cfg/commands_cfg_ripng.yaml") as f15:
    commands_cfg_ripng = yaml.safe_load(f15)
print(r1.cfg_ripv2(DEVICE_BM10, commands_cfg_ripng))
time.sleep(5)
result = ping('192.168.1.1')
while result is None:
    result = ping('192.168.1.1')
    print("DUT is rebooting, wait")
    time.sleep(5)
else:
    print("DUT up after reboot, wait all protocols!")
    time.sleep(25)
    print("All up!")
pytest.main(["-v", "-s", "--html=BULAT_TEST_BM10_RIPng.html", "../tests_all/test_check_ripng.py"])
