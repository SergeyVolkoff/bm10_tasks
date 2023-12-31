from base_bm10 import Base_bm10
import re
import sys
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
from rich.table import Table
from ping3 import ping, verbose_ping

class Cfg_templ_bm10(Base_bm10):
    
    def cfg_template(self,device,commands_template):

        """ФУНКЦИЯ-шаблон настройки базового конфига"""

        # self.check_connection(device)
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
            if "reboot" in command:
                time.sleep(5)
                result=ping('192.168.1.1',timeout=2)
                while result is None:
                    result=ping('192.168.1.1',timeout=2)
                    print("DUT is rebooting, wait")
                    time.sleep(5)
                else:
                    print("\nDUT up after reboot, wait all protocols!")
                    time.sleep(40)
                    print( "All up!")
            elif "Usage: uci [<options>] <command> [<arguments>]" in output:
                result_command = "bad command"
                print(command, result_command)
                result[command] = result_command
        return result

class Cfg_bm10(Cfg_templ_bm10):

    SLEEP_TIME5 = time.sleep(5)
    SLEEP_TIME10 = time.sleep(10)
    my_colors = Theme(
     #добавляет цветовую градацию для rich
    {
        "success":" bold green",
        "fail": "bold red",
        "info": "bold blue"
    }
)
    console = Console(theme=my_colors)
     
    def cfg_reset(self,device,commands_template):
        

        Cfg_templ_bm10.cfg_template(self,device,commands_template)
        return


    def cfg_base(self,device, commands_template):
        
        """ФУНКЦИЯ настройки базового конфига"""
        
        Cfg_templ_bm10.cfg_template(self,device,commands_template)
        return
        
         
    def cfg_base_802(self, device, commands_template):

        """ФУНКЦИЯ настройки stp- конфига"""

        Cfg_templ_bm10.cfg_template(self,device,commands_template)
        return


    def cfg_vlan(self,device,commands_template):

        """ФУНКЦИЯ настройки vlan- конфига (vlan-сабинтерфейc), после ребута потеря связи! """

        Cfg_templ_bm10.cfg_template(self,device,commands_template)
        return


    def cfg_WiFi_AP(self, device, commands_template):

        """ ФУНКЦИЯ настройки Wifi_AP """

        Cfg_templ_bm10.cfg_template(self,device, commands_template)
        return
    
    
    def cfg_3G(self, device, commands_template):

        """ ФУНКЦИЯ настройки 3G """

        Cfg_templ_bm10.cfg_template(self,device, commands_template)
        return


    def cfg_gre(self, device, commands_template):

        """ ФУНКЦИЯ настройки GRE """

        Cfg_templ_bm10.cfg_template(self,device, commands_template)
        return


    def cfg_pppoe_client(self,device,commands_template):

        """ ФУНКЦИЯ настройки роутера как РРРоЕ-клиент на wan порту
        Сначала залить сервер, потом - клиент """

        Cfg_templ_bm10.cfg_template(self,device,commands_template)
        return


    def cfg_pppoe_4(self,device,commands_template):

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

    def cfg_bgpv3(self, device, commands_template): 
        
        """ ФУНКЦИЯ настройки BGPv3 """

        Cfg_templ_bm10.cfg_template(self,device,commands_template)
        return
    

    def cfg_ospfv2(self, device,commands_template): 

        """ ФУНКЦИЯ настройки OSPFv2 """

        Cfg_templ_bm10.cfg_template(self,device,commands_template)
        return

    def cfg_mwan3(self, device,commands_template): 

        """ ФУНКЦИЯ настройки MWAN3 """

        Cfg_templ_bm10.cfg_template(self,device,commands_template)
        return
    
    def cfg_multihoming_failover(self, device,commands_template): 

        """ ФУНКЦИЯ настройки Multihoming """

        Cfg_templ_bm10.cfg_template(self,device,commands_template)
        return
    
    def cfg_pass (self,device, commands, log=True):

        """ ФУНКЦИЯ изменения пароля, надо поменять так,
        чтоб можно было вводить короткий пароль без сбоя и тащить пароль со стороны, а не из кода.
        без импорта"""
        
        # self.check_connection(device)
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
            # return output

  
        

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
        scp.put('../pppoe_cfg_file/pppoe', '/etc/config/')
        scp.close()
        self.client.close()
        print("File pppoe download")

    def cfg_pppoe_opt(self):

        """2-ФУНКЦИЯ настройки роутера как РРРоЕ-server на wan порту
        Сервр льем первым!
        эта ф-я передает файл pppoe-server-options в DUT, в файле лежит require-chaр,echo-interval"""
        
        # SCPCLient takes a paramiko transport as an argument
        scp = SCPClient(self.client.get_transport())
        scp.put('../pppoe_cfg_file/pppoe-server-options', '/etc/ppp/')
        scp.close()
        self.client.close()
        print("File pppoe-server-options download")
    
    def cfg_pppoe_chap(self):

        """3-ФУНКЦИЯ настройки роутера как РРРоЕ-server на wan порту
        Сервр льем первым!
        эта ф-я передает файл chap-secrets в DUT, в файле лежит login-pass"""
        
        # SCPCLient takes a paramiko transport as an argument
        scp = SCPClient(self.client.get_transport())
        scp.put('../pppoe_cfg_file/chap-secrets', '/etc/ppp/')
        scp.close()
        self.client.close()
        print("File chap-secrets download")

        
if __name__ == "__main__":
    with open("command_cfg/value_bm10.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Cfg_bm10(**device)
            r2 = SCP_cfg_ppoe()
            #print(r1.cfg_pass(device, commands='passwd'))                  # Cfg pass
            #print(r1.cfg_base(device,r1.commands_base_cfg))                # Cfg base_cfg (name, firewall,timezone,ASIIC,wifi, mwan)
            #print (r1.cfg_base_802(device, r1.commands_802_1d_cfg))        # Cfg for 802d (STP)
            #print(r1.cfg_vlan(device,r1.commands_vlan_cfg))                # Cfg for 802d (STP)
            #print(r1.cfg_WiFi_AP(device,r1.commands_cfg_WiFi_AP))          # Cfg wifi_ap (1-й порт не раздает!!!)
            #print(r1.cfg_pppoe_client(device,r1.commands_pppoe_client_cfg))# Cfg pppoe-client
            #print(r1.cfg_ripv2(device,r1.commands_cfg_ripv2))              # Cfg RIPv2+base_cfg
            #print(r1.cfg_ripvng(device,r1.commands_cfg_ripng))             # Cfg RIPng+base_cfg
            #print(r1.cfg_ospfv2(device,r1.commands_cfg_ospfv2))            # Cfg Ospfv2+base_cfg
            
            #print(r2.cfg_pppoe_serv())                                     # Cfg pppoe-serv1
            #print(r2.cfg_pppoe_opt())                                      # Cfg pppoe-serv2
            #print(r2.cfg_pppoe_chap())                                     # Cfg pppoe-serv3
            #print(r1.cfg_pppoe_4(device,r1.commands_pppoe_server_cfg))  # Cfg pppoe-serv4
            print(r1.cfg_pppoe_server_all)

            