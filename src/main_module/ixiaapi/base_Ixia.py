import re
import sys

from ixia_api import IxAPI


class Base_ixia():
    def __init__(self):
        self.ixiaApiServer = "127.0.0.1"
        self.ixiaApiPort = '11009'
        self.ixiaChassis = "10.27.193.3"
        self.connect = IxAPI(self.ixiaApiServer, self.ixiaApiPort)
        


    def connect_ixia(self):

        """ Подключение к IXIA. Загрузка конфигурационного файла (данные по API серверу указану в IxiaApi.py, файл ниже)"""
        
        self.connect.conn_srvr()
        self.connect.verif_sessions()
        file = "ixiaapi/cfgs_ixia/Cfg_access_trunk.ixncfg"
        #file = 'C:/Users/home/BULAT/TMP/Configs/IGMPv1_support.ixncfg'
        self.connect.load_conf(file)

if __name__=="__main__":
    ix= Base_ixia()
    print(ix.connect_ixia())