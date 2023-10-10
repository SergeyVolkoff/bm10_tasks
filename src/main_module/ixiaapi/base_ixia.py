import re
import sys
import requests

from ixia_api import IxAPI


class Base_ixia():
    def __init__(self):
        self.ixiaApiServer = "127.0.0.1"
        self.ixiaApiPort = '11009'
        self.ixiaChassis = "10.27.192.3"
        self.connect = IxAPI(self.ixiaApiServer, self.ixiaApiPort)
        self.conn_srvr = self.connect.conn_srvr()
        self.verif_sessions=self.connect.verif_sessions()


    def connect_ixia(self):

        """ Подключение к IXIA. Загрузка конфигурационного файла
          (данные по API серверу указану в IxiaApi.py, файл ниже)"""
        
        
        file = "ixiaapi/cfgs_ixia/Cfg_access_trunk.ixncfg"
        file = "C:/Users/user299/Desktop/Testing/ixia_test/cfgs_ixia/Cfg_access_trunk.ixncfg"
        self.connect.load_conf(file)
        try:
            self.response = requests.post(self.root+"/api/v1/sessions",
                         headers={'content-type': 'application/json'}, verify=False)
            if self.response.status_code == 201:
                print(f'Connection to IXAPI server {self.ipserver} is successfull')
        except Exception as error:
            print(error)

if __name__=="__main__":
    ix= Base_ixia()
    print(ix.connect_ixia())