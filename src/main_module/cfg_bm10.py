from base_bm10 import Base_bm10
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

        """ФУНКЦИЯ настройки vlan- конфига (vlan-сабинтерфейc), после ребута потеря связи! """

        Cfg_templ_bm10.cfg_template(self,device,commands_template)
        return


    def cfg_WiFi_AP(self, device, commands_template):

        """ ФУНКЦИЯ настройки Wifi_AP """

        Cfg_templ_bm10.cfg_template(self,device, commands_template)
        return
    

    def cfg_pppoe_client(self,device,commands_template):

        """ ФУНКЦИЯ настройки роутера как РРРоЕ-клиент на wan порту
        Сначала залить сервер, потом - клиент """

        Cfg_templ_bm10.cfg_template(self,device,commands_template)
        return


    def cfg_pppoe_serv(self,device,commands_template):

        """ 4-ФУНКЦИЯ настройки роутера как РРРоЕ-server на wan порту
        Сервр льем первым!
        эта ф-я передает донастривает рррое и имя на интерфейсе """
        
        Cfg_templ_bm10.cfg_template(self,device,commands_template)
        return
    

    def cfg_ripv2(self, device,commands_template):

        """ ФУНКЦИЯ настройки RIPv2 """

        Cfg_templ_bm10.cfg_template(self,device,commands_template)
        return
    

    def cfg_ripvng(self, device, commands_template): 
        
        """ ФУНКЦИЯ настройки RIPng """

        Cfg_templ_bm10.cfg_template(self,device,commands_template)
        return


    def cfg_ospfv2(self, device,commands_template): 

        """ ФУНКЦИЯ настройки OSPFv2 """

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

    
        
class SCP_cfg_ppoe(Cfg_templ_bm10):
    
    def __init__(self):
        
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # ключ добавится автоматом, без этого не соединится по ссх
        #self.client.load_system_host_keys()
        self.client.connect (
        hostname='192.168.1.1',
        username='root',
        password='root',
        port=22
        )
    def cfg_pppoe_serv(self):

        """1-ФУНКЦИЯ настройки роутера как РРРоЕ-server на wan порту
        Сервр льем первым!
        эта ф-я передает файл pppoe в DUT, в файле лежат настройки сервера ррре"""

        # SCPCLient takes a paramiko transport as an argument
        scp = SCPClient(self.client.get_transport())
        scp.put('src/main_module/pppoe_cfg_file/pppoe', '/etc/config/')
        scp.close()
        self.client.close()

    def cfg_pppoe_opt(self):

        """2-ФУНКЦИЯ настройки роутера как РРРоЕ-server на wan порту
        Сервр льем первым!
        эта ф-я передает файл pppoe-server-options в DUT, в файле лежит require-chaр,echo-interval"""
        
        # SCPCLient takes a paramiko transport as an argument
        scp = SCPClient(self.client.get_transport())
        scp.put('src/main_module/main_module/pppoe_cfg_file/pppoe-server-options', '/etc/ppp/')
        scp.close()
        self.client.close()
    
    def cfg_pppoe_chap(self):

        """3-ФУНКЦИЯ настройки роутера как РРРоЕ-server на wan порту
        Сервр льем первым!
        эта ф-я передает файл chap-secrets в DUT, в файле лежит login-pass"""
        
        # SCPCLient takes a paramiko transport as an argument
        scp = SCPClient(self.client.get_transport())
        scp.put('src/main_module/pppoe_cfg_file/chap-secrets', '/etc/ppp/')
        scp.close()
        self.client.close()

        
if __name__ == "__main__":
    with open("command_cfg/value_bm10.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Cfg_bm10(**device)
            r2 = SCP_cfg_ppoe()
            #print(r1.cfg_pass(device, commands='passwd'))
            #print(r1.cfg_base(device,r1.commands_base_cfg))
            #print (r1.cfg_base_802(device, r1.commands_802_1d_cfg))
            print(r1.cfg_base(device, r1.commands_base_cfg))
            #print(r1.cfg_base_802(device, r1.commands_802_1d_cfg))
            #print(r1.cfg_vlan(device,r1.commands_vlan_cfg))
            #print(r1.cfg_WiFi_AP(device,r1.commands_cfg_WiFi_AP))
            #print(r1.cfg_pppoe_client(device,r1.commands_pppoe_client_cfg))
            #print(r1.cfg_ripv2(device,r1.commands_cfg_ripv2))
            #print(r1.cfg_ripvng(device,r1.commands_cfg_ripng))
            #print(r1.cfg_ospfv2(device,r1.commands_cfg_ospfv2))
            


            #print(r2.cfg_pppoe_serv())
            #print(r2.cfg_pppoe_opt())
            #print(r2.cfg_pppoe_chap())
            #print(r1.cfg_pppoe_serv(device,r1.commands_pppoe_server_cfg))