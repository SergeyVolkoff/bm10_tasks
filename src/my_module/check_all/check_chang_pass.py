
import sys
import os
import time
import yaml
sys.path.insert(1, os.path.join(sys.path[0],'..'))  # !!! PATH fo import with position 1!!!
from cfg_bm10 import Cfg_bm10
from tests_all.test_check_chang_pass import new_pass

def cfg_pass_new(pass_for_test):

    """ ФУНКЦИЯ изменения пароля"""
    
    device = {
        'device_type': 'linux',
        'host': '192.168.1.1',
        'username': 'root',
        'password': f"{pass_for_test}",
        'timeout': 1}
    new_pass_list = list(new_pass)
    index_pass = new_pass_list.index(pass_for_test)
    if pass_for_test !='root':
        index_new_pass = index_pass-1
        reverse_pss=new_pass_list[index_new_pass]
        print(pass_for_test)
        print('******reverse_pss=',reverse_pss)
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
    r2 = Cfg_bm10(**device)
    prompt = r2.ssh.find_prompt()
    commands='passwd'
    time.sleep(5)
    output = r2.ssh.send_command(commands, expect_string="New password:", read_timeout=2)
    print(output, "****")

    if "New" in output:
        output = r2.ssh.send_command_timing(pass_for_test, read_timeout=1)
        print(output, "****")
        if "Bad password" not in output:
            return False

        else:
            output = r2.ssh.send_command_timing(pass_for_test, read_timeout=1)
            r2.console.print(output,style="success")
        if "Re-enter new password:" in output:
            output = r2.ssh.send_command_timing(pass_for_test, read_timeout=1)
            r2.console.print(output,style="warning")
            while True:
                if "root@" not in output:
                    output = r2.ssh.read_until_pattern(f'{prompt}', read_timeout=0)
                    print("Wait, the password will change now")
                    r2.ssh.write_channel(" ")
                elif "root@" in output:
                    r2.console.print("New pass OK",style="success")
                    return True
                

if __name__ == "__main__":
    result = check_chang_pass()
    print(result)