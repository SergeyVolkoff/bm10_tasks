# -*- coding: utf-8 -*-
import re
import sys
import yaml
import netmiko
import paramiko
import time


from ping3 import ping, verbose_ping
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
#from netmiko.linux.linux_ssh import LinuxSSH
my_colors = Theme( #добавляет цветовую градацию для rich
    {
        "success":"bold green",
        "fail":"bold red",
        "warning":"bold yellow"
    }
)
console = Console(theme=my_colors)

class Base_bm10():
    def __init__(self,host, username, timeout, password,**kwargs):
        try:
            with open("command_cfg/value_bm10.yaml") as f2:
                temp = yaml.safe_load(f2)
                for t in temp:
                     device = dict(t)
            with open ("command_cfg/commands_reset_cfg.yaml") as f1:            # команды сброса конфига
                self.commands_to_reset_conf = yaml.safe_load(f1)
            with open("command_cfg/commands_cfg_3G.yaml") as f:                 # команды настройки 3G
                self.commands_cfg_3G = yaml.safe_load(f)
            with open ("command_cfg/commands_base_cfg.yaml") as f3:             # команды настройки базового конфига(хост,firewall,wifi)
                self.commands_base_cfg = yaml.safe_load(f3)
            with open ("command_cfg/commands_802_1d_cfg.yaml") as f4:           # команды настройки STP+ базовые настройки
                self.commands_802_1d_cfg = yaml.safe_load(f4)
            with open ("command_cfg/commands_gre_config.yaml") as f5:           # команды настройки GRE-tun + базовые настройки
                self.commands_gre_config = yaml.safe_load(f5)
            with open("command_cfg/commands_Fwall_cfg.yaml") as f6:             # команды настройки firewall wan2(как замена порта)
                self.commands_Fwall_cfg = yaml.safe_load(f6)
            with open("command_cfg/commands_dmz_cfg.yaml") as f7:               # команды настройки DMZ доделать правило трафика!!!
                self.commands_dmz_cfg = yaml.safe_load(f7)
            with open("command_cfg/commands_reset_cfg.yaml") as f8:             # команды настройки reset
                self.commands_reset_cfg = yaml.safe_load(f8)
            with open("command_cfg/commands_sh_base.yaml") as f9:               # команды настройки base_cfg
                self.commands_sh_base = yaml.safe_load(f9)
            with open("command_cfg/commands_vlan_cfg.yaml") as f10:              # команды настройки vlan_cfg
                self.commands_vlan_cfg = yaml.safe_load(f10)
            with open("command_cfg/commands_cfg_WiFi_AP.yaml") as f11:            #  команды настройки wifi_ap
                self.commands_cfg_WiFi_AP = yaml.safe_load(f11)
            with open("command_cfg/commands_cfg_WiFi_AP_KingKong.yaml") as f12:    # команды настройки wifi_ap2
                self.commands_cfg_WiFi_AP_KingKong = yaml.safe_load(f12)
            with open("command_cfg/commands_pppoe_client_cfg.yaml") as f13:        # команды настройки РРРРоЕ-клиент
                self.commands_pppoe_client_cfg = yaml.safe_load(f13)
            with open("command_cfg/commands_pppoe_server_cfg.yaml") as f14:         # команды настройки РРРРоЕ-server
                self.commands_pppoe_server_cfg = yaml.safe_load(f14)
            with open("command_cfg/commands_cfg_ripv2.yaml") as f15:                # команды настройки Ripv2
                self.commands_cfg_ripv2 = yaml.safe_load(f15)
            with open("command_cfg/commands_cfg_ripng.yaml") as f16:                # команды настройки Ripng
                self.commands_cfg_ripng = yaml.safe_load(f16)
            with open("command_cfg/commands_cfg_ospfv2.yaml") as f17:
                self.commands_cfg_ospfv2 = yaml.safe_load(f17)
            with open("command_cfg/commands_cfg_bgpv3.yaml") as f18:
                self.commands_cfg_bgpv3 = yaml.safe_load(f18)
            self.ssh = ConnectHandler(**device)
            self.ip = host
            self.name = username
            self.passwd = password
            self.promo_ping = " -w 4"
            self.promt_tracert = '-m 3'
            self.word_ping = "ping "
            self.ip_inet = "8.8.8.8"
            #self.command_ping = self.word_ping+self.promo_ping
        except(NetmikoAuthenticationException,NetmikoTimeoutException) as error:
            print("*" * 5, "Error connection to:", device['host'], "*" * 5)
    my_colors = Theme( #добавляет цветовую градацию для rich
    {
        "success":"bold green",
        "fail":"bold red",
        "warning":"bold yellow"
    }
    )   
    console = Console(theme=my_colors)

    def check_connection(self,device,log=True):

        """
        ФУНКЦИЯ проверки установки соединения с роутером
        """

        if log:
            console.print(f"Try connect to {device['host']}...", style="warning")
        try:
            with ConnectHandler(**device) as ssh:
                console.print(device['host'], "connected!", style='success')
        except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
            console.print("*" * 5, "Error connection to:", device['host'], "*" * 5, style='fail')


    def send_command(self, device, command):

        """ФУНКЦИЯ отправки простой команды в уст-во по ssh, без импорта"""

        #self.check_connection(device)         # вызов функции проверки соединения с роутером
        temp = self.ssh.send_command(command)
        result = temp
        return result
    

    def ping_inet(self, device):

        """ФУНКЦИЯ для простого пинга 8.8.8.8 , формат команды прописан в инит.
        без импорта."""

        self.check_connection(device)
        command_ping = (self.word_ping + self.ip_inet + self.promo_ping)
        print(command_ping)
        output = self.ssh.send_command(command_ping)
        if "round-trip min/avg/max" in output:
            output = re.search(r'round-trip min/avg/max = (\S+ ..)', output).group()
            result = ["IP", self.ip_inet, "destination available :", output]
            result = ' '.join(result)
        else:
            result = ["Ip", self.ip_inet, "out of destination"]
            result = ' '.join(result)
        return result
        print(output)

    def tracert_inet(self,device):

        """ФУНКЦИЯ для  tracert 8.8.8.8 for pppoe peer!!!"""

        comand_tracert = f'traceroute {self.ip_inet} {self.promt_tracert}'
        output_tracert = self.ssh.send_command(comand_tracert)
        if "ms" in output_tracert:
            temp = self.send_command(device,'ip a')
            if "peer" in temp:
                output1 = re.search(r'\s+inet (?P<ip_int>\d+.\d+.\d+.\d+) peer (?P<ip_peer>\d+.\d+.\d+.\d+).{0,}pppoe-wan',
                                temp)
                ip_peer = output1.group('ip_peer')
                result = f'### Tracert passes through server-peer, {ip_peer}! ###\n {output_tracert}'
            else:
                result = f'### Tracert passes! ###\n {output_tracert}'
        else:
            result = f'Tracert does not pass through {output_tracert}'

        return result
        print(output)
        
    def ping_ip(self, device,ip_for_ping):
        
        """ФУНКЦИЯ для простого пинга,  запросит адрес назначения, формат команды прописан в инит.
        без импорта."""

        self.check_connection(device)
        command_ping = (self.word_ping + ip_for_ping + self.promo_ping)
        print(command_ping)
        output = self.ssh.send_command(command_ping)
        if "round-trip min/avg/max" in output:
            output = re.search(r'round-trip min/avg/max = (\S+ ..)', output).group()
            result = ["IP", ip_for_ping, "destination available :", output]
            result = ' '.join(result)
        else:
            result = ["Ip", ip_for_ping, "out of destination"]
            result = ' '.join(result)
        return result
        print(output)


    def tracert_ip(self,device,ip_tracert):

        """ФУНКЦИЯ для  tracert ip"""

        #self.check_connection(device)
        comand_tracert = f'traceroute {ip_tracert} {self.promt_tracert}'
        output_tracert = self.ssh.send_command(comand_tracert)
        if "ms" in output_tracert:
            temp = self.send_command(device,'ip a')
            if "peer" in temp:
                output1 = re.search(r'\s+inet (?P<ip_int>\d+.\d+.\d+.\d+) peer (?P<ip_peer>\d+.\d+.\d+.\d+).{0,}pppoe-wan', temp)
                ip_peer = output1.group('ip_peer')
                result = f'### Tracert passes through server-peer, {ip_peer}! ###\n {output_tracert}'
            else:
                result = f'### Tracert passes! ###\n {output_tracert}'
        else:
            result = f'Tracert does not pass through {output_tracert}'

        return result
        print(output)


    def reset_conf(self,device, comm_reset_conf):
        
        """ ФУНКЦИЯ сброса конфига на заводской, с ребутом устр-ва.
        без импорта
        """

        self.check_connection(device)
        output = self.ssh.send_command("uci show system.@system[0].hostname")
        print(output)
        if "DUT" in output:
            result_reset=self.ssh.send_config_set(self.commands_to_reset_conf)
            return result_reset
        

    def wait_reboot(self):
        result=ping('192.168.1.1')
        while result is None:
            result=ping('192.168.1.1')
            print(result)
            print("DUT in reboot, weit!")
            time.sleep(5)
        else:
            print("DUT up after reboot, weit all protocols!")
            time.sleep(5)
            return "all up!"


if __name__ == "__main__":
    with open("command_cfg/value_bm10.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Base_bm10(**device)
            #print(r1.send_command(device, "uci show"))
            #print(r1.ping_inet(device))
            #print(r1.ping_ip(device,'8.8.8.8'))
            #print (r1.wait_reboot())
            print(r1.check_connection(device))