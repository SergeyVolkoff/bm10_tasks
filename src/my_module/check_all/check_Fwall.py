import re
import time
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from base_bm10 import Base_bm10


def check_Fwall():

    """
    Проверка зоны firewall, настраиваем 4 порт как ван, 
    открываем инпут в firewall,  пингуем с соседа
    """

    with open("/home/ssw/Documents/bm10_tasks/src/my_module/command_cfg/value_bm10.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Base_bm10(**device)
    try:
        time.sleep(0)
        res={}
        for command in r1.commands_Fwall_cfg:  #отправляем конфиг фаервола
            output = r1.ssh.send_command(command, expect_string="", read_timeout=1)
            time.sleep(1)
            if "" in output:
                output = "command passed"
                res[command] = output
            elif "Usage: uci [<options>] <command> [<arguments>]" in output:
                output = "bad command"
                res[command] = output
        print(res)

        temp2 = r1.ping_ip(device,r1.command_ping)              # проверяем доступность соседа
        if "destination  available " in temp2:               #если отвечает, значит firewall зона настроена правильно.
            return True
        else:
            if " out of destination" in temp2:            #если не отвечает - не правльно настроена зона firewall.
                return False
    except ValueError as err:
        return False

if __name__ == "__main__":
     result = check_Fwall()
     print(result)