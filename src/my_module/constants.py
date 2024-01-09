import yaml
import time

from rich import print
from rich.theme import Theme
from rich.console import Console
from pprint import pprint

with open("../command_cfg/value_bm10.yaml")as f:
    temp = yaml.safe_load(f)
    for t in temp:
        DEVICE_BM10 = dict(t)

with open("../command_cfg/commands_reset_cfg.yaml") as f14:  # команды сброса конфига
        RESET_CONFIG_COMMAND = yaml.safe_load(f14)

my_colors = Theme(
     #добавляет цветовую градацию для rich
    {
        "success":" bold green",
        "fail": "bold red",
        "info": "bold blue"
    }
)
CONSOLE = Console(theme=my_colors)