import pytest
from check_all.check_mwan3 import *

def test_check_enable_mwan3():
    assert check_enable_mwan3() ==True, "MWAN3 status - disable!"

def test_check_tracert_when_mwan3_disable():
    assert check_trsrt_mwan_stop()==True, "hop with an address 192.168.10.2 and 192.168.20.2 in the tracert!!!"