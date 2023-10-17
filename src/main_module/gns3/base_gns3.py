
from gns3fy import Gns3Connector, Project, Node, Link
from tabulate import tabulate

class Base_gns():

    
    def __init__(self):

        """ Определение коннектора(connector) и проекта (lab) """

        self.server_url = "http://10.27.193.245:3080"
        self.connector = Gns3Connector(url=self.server_url)
        self.list_labs = (tabulate(self.connector.projects_summary(is_print=False), headers=["Project Name"]))
        print(self.list_labs)
        self.name_lab = input("Input lab name: ")
        

    def all_proj (self):

        """ Возвращает перечень всех лаб в ГНС"""

        return tabulate(
            self.connector.projects_summary(is_print=False),
            headers=["Project Name", "Project ID", "Total Nodes", "Total Links", "Status"],
        )

    def get_ver_gns(self):

        """ Вернет версию GNS - абсолютно бесполезная хрень, если выкл обновление """

        gns_ver = self.connector.get_version()
        return f"GNS3 ver is {gns_ver}"
        
    def get_lab(self):

        """ Вернет lab_id, статус моей лабы """

        lab = Project(name=self.name_lab , connector=self.connector )
        print(lab.project_id)
        return f"GNS3 lab_name: {lab.name}, lab_id:{lab.project_id}, lab status: {self.lab.status}"
    
    def get_nodes(self):

        """ Вернет все узлы в лабе"""

        lab = Project(name=self.name_lab , connector=self.connector )
        lab.open() # open lab
        
        print(f"*** ALL nodes in {lab.name} lab ***")
        return  lab.nodes_summary()
    
    def start_node(self):

        """ Запуск 1 узла в проекте"""
        lab = Project(name=self.name_lab , connector=self.connector )
        r1 = Node(
            project_id=lab.project_id, 
            name='R1',
            connector=self.connector
            ) # создаем экз-р устр-ва
        
        r1.get()
        stts_ret=r1.start()
        return stts_ret

    def start_nodes_from_project(self):

        lab = Project(name=self.name_lab , connector=self.connector )
        lab_get = lab.get()

        print(lab)
        print(lab_get)
        lab.open()
        print(lab.status)
        result_starta=lab.start_nodes(poll_wait_time=5)
        return lab.status

if __name__=="__main__":
    gns= Base_gns()
    # print (gns.get_ver_gns(),'\n')
    # print(gns.all_proj(),'\n')
    # print(gns.get_lab(),'\n')
    # print( gns.get_nodes(),'\n')
    # print(gns.start_node())
    print(gns.start_nodes_from_project())
