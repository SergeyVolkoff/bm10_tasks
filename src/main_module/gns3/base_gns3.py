
from gns3fy import Gns3Connector, Project, Node, Link
from tabulate import tabulate

class Base_gns():
    def __init__(self):

        """ Определение коннектора(connector) и проекта (lab) """

        self.server_url = "http://10.27.193.245:3080"
        self.connector = Gns3Connector(url=self.server_url)
        self.lab = Project(name="SSV_test", connector=self.connector )
    
    def all_proj (self):

        """ Возвращает перечень всех лаб в ГНС"""

        return tabulate(
            self.connector.projects_summary(is_print=False),
            headers=["Project Name", "Project ID", "Total Nodes", "Total Links", "Status"],
        )

    def get_ver_gns(self):

        """ Вернет версию - абсолютно бесполезная хрень, если выкл обновление """

        gns_ver = self.connector.get_version()
        return f"GNS3 ver is {gns_ver}"

    def get_lab(self):

        """ Вернет lab_id, статус моей лабы """

        self.lab.get()
        print(self.lab.project_id)
        return f"GNS3 lab_name: {self.lab.name}, lab_id:{self.lab.project_id}, lab status: {self.lab.status}"
    
    def get_nodes(self):

        """ Вернет все узлы в лабе"""

        self.lab.open()
        print(f"*** ALL nodes in {gns.lab.name} lab ***")
        return  self.lab.nodes_summary()
    
    def start_nod(self):
        self.lab.get()
        r1=Node(project_id=self.lab.project_id, name='R1',connector=self.connector)
        r1.get()
        stts_ret=r1.start()
        return stts_ret

        
    
if __name__=="__main__":
    gns= Base_gns()
    #print (gns.get_ver_gns(),'\n')
    #print(gns.all_proj(),'\n')
    #print(gns.get_lab(),'\n')
    #print( gns.get_nodes(),'\n')
    print(gns.start_nod())