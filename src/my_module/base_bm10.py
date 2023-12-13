# -*- coding: utf-8 -*-
import re
import os
import sys
import pprint
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
from netmiko.linux.linux_ssh import LinuxSSH
my_colors = Theme( #добавляет цветовую градацию для rich
    {
        "success":"bold green",
        "fail":"bold red",
        "info": "bold blue"
    }
)
console = Console(theme=my_colors)

class Base_bm10():
    def __init__(self,host, username, timeout, password,**kwargs):
        with open("../command_cfg/value_bm10.yaml") as f2:
            temp = yaml.safe_load(f2)
            for t in temp:
                    device = dict(t)
                    
                    self.check_connection(device)
        self.ssh = ConnectHandler(**device)
        self.ip = host
        self.name = username
        self.passwd = password
        self.promo_ping = " -w 4"
        self.promt_tracert = '-m 5'
        self.word_ping = "ping "
        self.ip_inet = "8.8.8.8"
        #self.command_ping = self.word_ping+self.promo_ping
       

    def check_connection(self,device,log=True):

        """
        ФУНКЦИЯ проверки установки соединения с роутером
        """

        if log:
            console.print(f"Try connect to {device['host']}...", style="info")
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

        #self.check_connection(device)
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

        #self.check_connection(device)
        command_ping = (self.word_ping + ip_for_ping + self.promo_ping)
        output = self.ssh.send_command(command_ping)
        if "round-trip min/avg/max" in output:
            output = re.search(r'round-trip min/avg/max = (\S+ ..)', output).group()
            result = ["IP", ip_for_ping, "destination available :", output]
            result = ' '.join(result)
        else:
            result = ["Ip", ip_for_ping, "out of destination"]
            result = ' '.join(result)
        return result


    def tracert_ip(self,device,ip_tracert):

        """ФУНКЦИЯ для  tracert ip"""

        #self.check_connection(device)
        comand_tracert = f'traceroute {ip_tracert} {self.promt_tracert}'
        output_tracert = self.ssh.send_command(comand_tracert, read_timeout=25)
        # if "ms" in output_tracert:
        #     temp = self.send_command(device,'ip a')
        #     if "peer" in temp:
        #         output1 = re.search(r'\s+inet (?P<ip_int>\d+.\d+.\d+.\d+) peer (?P<ip_peer>\d+.\d+.\d+.\d+).{0,}pppoe-wan', temp)
        #         ip_peer = output1.group('ip_peer')
        #         result = f'### Tracert passes through server-peer, {ip_peer}! ###\n {output_tracert}'
        #     else:
        #         result = f'### Tracert passes! ###\n {output_tracert}'
        # else:
        #     result = f'Tracert does not pass  {output_tracert}'

        return output_tracert


    def reset_conf(self,device):
        
        """ ФУНКЦИЯ сброса конфига на заводской, с ребутом устр-ва."""

        # self.check_connection(device)
        output = self.ssh.send_command("uci show system.@system[0].hostname")
        print(output)
        
        if "DUT" in output:
            result_reset=self.ssh.send_config_set(self.commands_to_reset_conf)
            result=ping('192.168.1.1')
            while result is None:
                result=ping('192.168.1.1')
                print("DUT is rebooting, wait")
                time.sleep(5)
            else:
                print("DUT up after reboot, wait all protocols!")
                time.sleep(25)
                print( "All up!")
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
            # print(r1.send_command(device, "uci show"))
            #print(r1.ping_inet(device))
            #print(r1.ping_ip(device,'8.8.8.8'))
            #print (r1.wait_reboot())
            #print(r1.check_connection(device))
            print(r1.reset_conf(device))