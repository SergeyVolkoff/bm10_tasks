from Base_bm10 import Base_bm10
import re
import yaml
import netmiko
import paramiko
import time
from paramiko import SSHClient
from scp import SCPClient
from rich import print
from rich.theme import Theme
from rich.console import Console
from pprint import pprint
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException
)
from rich.console import Console
from rich.table import Table
from netmiko.linux.linux_ssh import LinuxSSH
from rich.table import Table
from rich.console import Console
from rich.theme import Theme



class Cfg_BM10(Base_bm10):
    

    def cfg_pass (self,device, commands, log=True):

            """ ФУНКЦИЯ изменения пароля, надо поменять так,
            чтоб можно было вводить короткий пароль без сбоя и тащить пароль со стороны, а не из кода.
            без импорта"""
            
            # if log:
            #     self.console.print(f"Connect to {device['host']}...",style="success") # style переменная rich, назначает цвет выводу
            # result = ''
            # try:
            #     with ConnectHandler(**device) as ssh:
            new_pass = input("Input new pass: ")
            prompt = self.ssh.find_prompt()
            output = self.ssh.send_command(commands, expect_string="New password:", read_timeout=2)
            print(output, "****")
            if "New" in output:
                output = self.ssh.send_command_timing(new_pass, read_timeout=1)
                print(output, "****")
                if "Bad password" not in output:
                    pass
                else:
                    output = self.ssh.send_command_timing(new_pass, read_timeout=1)
                    self.console.print(output,style="success")
                if "Re-enter new password:" in output:
                    output = self.ssh.send_command_timing(new_pass, read_timeout=1)
                    self.console.print(output,style="warning")
                    while True:
                        if "root@" not in output:
                            output = self.ssh.read_until_pattern(f'{prompt}', read_timeout=0)
                            print("Wait, the password will change now")
                            self.ssh.write_channel(" ")
                        elif "root@" in output:
                            self.console.print("New pass OK",style="success")
                            break
                return output
            # except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
            #     print("*" * 5, "Error connection to:", device['host'], "*" * 5)




if __name__ == "__main__":
    with open("src/BM10_LTE.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Cfg_BM10(**device)
            print(r1.cfg_pass(device, commands='passwd'))
            