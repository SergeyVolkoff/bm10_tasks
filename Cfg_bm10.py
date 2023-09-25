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



class Cfg_templ_bm10(Base_bm10):
    
    def cfg_template(self,device,commands_template):

        """ФУНКЦИЯ настройки базового конфига"""

        self.check_connection(device)
        result = {}
        for command in commands_template:
            output = self.ssh.send_command(command, expect_string="", read_timeout=1)
            if "mwan3" in command:
                    result_command = "wait, please"
                    print(command, result_command)
                    time.sleep(3)
            if "commit" in command:
                result_command = "wait, please"
                print(command, result_command)
                time.sleep(3)
            if "" in output:
                result_command = "command passed"
                result[command]=output
                print(command,result_command)
            elif "Usage: uci [<options>] <command> [<arguments>]" in output:
                result_command = "bad command"
                print(command, result_command)
                result[command] = result_command
        return result

class Cfg_bm10(Cfg_templ_bm10):
     

    def cfg_base(self,device, commands_template):
        
        """ФУНКЦИЯ настройки базового конфига"""
        # super().cfg_template(self,device,commands_template) # checkeed!!!!
        Cfg_templ_bm10.cfg_template(self,device,commands_template)
        return
        
         
    def cfg_base_802(self, device, commands_template):

        """ФУНКЦИЯ настройки stp- конфига"""

        Cfg_templ_bm10.cfg_template(self,device,commands_template)
        return


    def cfg_vlan(self,deice,commands_template):

        """ФУНКЦИЯ настройки vlan- конфига (vlan-сабинтерфейc)"""

        Cfg_templ_bm10.cfg_template(self,device,commands_template)
        return


    def cfg_pass (self,device, commands, log=True):

        """ ФУНКЦИЯ изменения пароля, надо поменять так,
        чтоб можно было вводить короткий пароль без сбоя и тащить пароль со стороны, а не из кода.
        без импорта"""
        
        self.check_connection(device)
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
        

if __name__ == "__main__":
    with open("src/BM10_LTE.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Cfg_bm10(**device)
            #print(r1.cfg_pass(device, commands='passwd'))
            #print(r1.cfg_base(device,r1.commands_base_cfg))
            #print (r1.cfg_base_802(device, r1.commands_802_1d_cfg))
            print(r1.cfg_base(device, commands_template=r1.commands_base_cfg))
            #print(r1.cfg_base_802(device, commands_template=r1.commands_802_1d_cfg))
            #print(r1.cfg_vlan(device,commands_template=r1.commands_vlan_cfg))