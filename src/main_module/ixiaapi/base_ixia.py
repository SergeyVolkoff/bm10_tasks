import re
import sys
import requests

from ixia_api import IxAPI


class Base_ixia():
    def __init__(self):
        self.ixiaApiServer = "10.27.192.176"
        self.ixiaApiPort = '11009'
        self.ixiaChassis = "10.27.192.3"
        self.connect = IxAPI(self.ixiaApiServer, self.ixiaApiPort)
        self.conn_srvr = self.connect.conn_srvr()
        self.verif_sessions=self.connect.verif_sessions()


    def connect_ixia(self):

        """ Подключение к IXIA. Загрузка конфигурационного файла 
		(данные по API серверу указану в IxiaApi.py, файл выше)"""
        
        self.connect.conn_srvr()
        self.connect.verif_sessions()
        file = "C:/Users/user299/Desktop/Testing/ixia_test/cfgs_ixia/Cfg_access_trunk.ixncfg"
        self.connect.load_conf(file)

if __name__=="__main__":
    ix= Base_ixia()
    print(ix.connect_ixia())