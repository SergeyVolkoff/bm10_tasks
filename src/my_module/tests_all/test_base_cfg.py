import re
import sys

import yaml
import netmiko
import pytest
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from check_all.check_base_cfg import *


def test_enable_support_ASIC():
    assert check_sup_ASIC(
        "uci show firewall.@defaults[0].flow_offloading_hw") == True, "Firewall offloading_hw  disable"

def test_enable_firewall_zone_wan():
    assert check_firewall("uci show firewall.@zone[1].forward") == True, "Firewall.@zone[1].forward disable"

def test_enable_name_device():
    assert check_name_dev("uci show system.@system[0].hostname") == True, "Name device is wrong"

def test_check_zone_time():
    assert check_time_zone("uci show system.@system[0].zonename") == True, "Time zone wrong"

def test_check_ntp():
    assert check_ntp("uci show system.ntp.server") == True, "NTP server not configure"
def test_wifi_name():
    assert check_wifi_name("uci show wireless.default_radio0.ssid")==True, "Wifi name wrong"

def test_mwan3_on():
    assert check_mwan3("mwan3 status")==True, "Mwan3 ON!!!"



# def test_name_device():
#     assert check_name_device("uci show system.@system[0].hostname")=True, "sdf"

