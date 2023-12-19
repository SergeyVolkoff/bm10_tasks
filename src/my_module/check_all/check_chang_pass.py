
import sys
import os
import time
import yaml
sys.path.insert(1, os.path.join(sys.path[0],'..'))  # !!! PATH fo import with position 1!!!
from cfg_bm10 import Cfg_bm10
from tests_all.test_check_chang_pass import new_pass
from netmiko import (
    ConnectHandler,
    NetmikoAuthenticationException
    )
def cfg_pass_new(pass_for_test):

    """ ФУНКЦИЯ изменения пароля"""
    

    new_pass_list = list(new_pass)
    index_pass = new_pass_list.index(pass_for_test)
    if index_pass > 0:
        index_new_pass = index_pass-1
        reverse_pss=new_pass_list[index_new_pass]
        
        device = {
                    'device_type': 'linux',
                    'host': '192.168.1.1',
                    'username': 'root',
                    'password': reverse_pss,
                    'timeout': 1}
    else:
        device = {
                    'device_type': 'linux',
                    'host': '192.168.1.1',
                    'username': 'root',
                    'password': 'root',
                    'timeout': 1}
    ssh = ConnectHandler(**device)
    # r2 = Cfg_bm10(**device)
    commands='passwd'
    output = ssh.send_command(commands, expect_string="New password:", read_timeout=2)
    print('Password for test =',pass_for_test)
    if "New" in output:
        output = ssh.send_command_timing(pass_for_test, read_timeout=1)
        if "Bad password" not in output:
                pass
            
        # else:
        #     output = r2.ssh.send_command_timing(pass_for_test, read_timeout=1)
        #     r2.console.print(output,style="success")
        if "Re-enter new password:" or 'Retype password:' in output:
            output = ssh.send_command_timing(pass_for_test, read_timeout=1)
            prompt = ssh.find_prompt()
            if "root@" not in prompt:
                print("Wait, the password will change now")
                time.sleep(3)
            elif "root@" in prompt:
                print(f"Tested password {pass_for_test} OK\n")
                ssh.disconnect
                return True
    


# if __name__ == "__main__":
#     result = cfg_pass_new()
#     print(result)