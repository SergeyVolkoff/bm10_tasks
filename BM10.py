# -*- coding: utf-8 -*-
import re
import yaml
import netmiko
import paramiko
import time
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



class BM10():
    def __init__(self, device_type, host, username, timeout, password,**kwargs):
        try:
            with open("src/BM10_LTE.yaml") as f2:
                temp = yaml.safe_load(f2)
                for t in temp:
                    device = dict(t)
            self.ssh = ConnectHandler(**device)
            self.ip = host
            self.name = username
            self.passwd = password
            self.promo_ping = " -w 4"
            self.promt_tracert = '-m 3'
            self.word_ping = "ping "
            self.command_ping = self.word_ping+self.promo_ping
        except(NetmikoAuthenticationException,NetmikoTimeoutException) as error:
            print("*" * 5, "Error connection to:", device['host'], "*" * 5)


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

        """ФУНКЦИЯ для простого пинга,  запросит адрес назначения, формат команды прописан в инит.
        без импорта."""

        self.check_connection(device)
        ip_for_ping = "8.8.8.8"
        command_ping = (self.word_ping + ip_for_ping + self.promo_ip)
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


    def ping_ip(self, device,ip_for_ping):

        """ФУНКЦИЯ для простого пинга,  запросит адрес назначения, формат команды прописан в инит.
        без импорта."""

        self.check_connection(device)
        command_ping = (self.word_ping + ip_for_ping + self.promo_ip)
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


    def tracert_inet(self,device):

        """ФУНКЦИЯ для  tracert 8.8.8.8 for pppoe peer!!!"""

        ip_tracert = '8.8.8.8'
        comand_tracert = f'traceroute {ip_tracert} {self.promt_tracert}'
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


    def tracert_ip(self,device,ip_tracert):

        """ФУНКЦИЯ для  tracert ip"""

        #self.check_connection(device)
        comand_tracert = f'traceroute {ip_tracert} {self.promt_tracert}'
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
        

if __name__ == "__main__":
    with open("src/BM10_LTE.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = BM10(**device)
            #print(r1.send_command(device, "uci show"))
            print(r1.tracert_ip(device,ip_tracert='8.8.8.8'))



