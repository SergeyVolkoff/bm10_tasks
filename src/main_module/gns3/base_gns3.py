import re
import sys
import requests
from gns3fy import Gns3Connector, Project, Node, Link
from tabulate import tabulate

class Base_gns():
    def __init__(self):
        self.server_url = "http://10.27.193.245:3080"
        self.connector = Gns3Connector(url=self.server_url)
        self.lab = Project(name="SSV_test", connector=self.connector )
    
    def all_proj (self):
        return tabulate(
            self.connector.projects_summary(is_print=False),
            headers=["Project Name", "Project ID", "Total Nodes", "Total Links", "Status"],
        )

    def get_ver_gns(self):
        gns_ver = self.connector.get_version()
        return f"GNS3 ver is {gns_ver}"

    def get_lab(self):
        #lab = Project(name="SSV_test", connector=self.connector)
        self.lab.get()
        return f"GNS3 {self.lab.name} lab status: {self.lab.status}"
    
    def get_nodes(self):
        self.lab.open()
        print(f"*** nodes{gns.lab.name} lab ***")
        return  self.lab.nodes_summary()
    
    # def get_nod(self):
    #     return (self.lab.get_node("Cloud1"))
        
    
if __name__=="__main__":
    gns= Base_gns()
    print (gns.get_ver_gns())
    print(gns.all_proj())
    print(gns.get_lab())
    print( gns.get_nodes())
    # print (gns.get_nod())
