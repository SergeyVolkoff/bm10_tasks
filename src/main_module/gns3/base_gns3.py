from gns3fy import Gns3Connector, Project, Node, Link

class Base_gns():
    def __init__(self):
        self.server_url = "http://10.27.193.245:3080"
        self.connector = Gns3Connector(url=self.server_url)

    def connect_gns(self):
        return self.connector.get_version()

if __name__=="__main__":
    gns= Base_gns()
    print (f"return ver GNS: {gns.connect_gns()}")
