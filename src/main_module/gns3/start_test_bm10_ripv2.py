from base_gns3 import Base_gns
import yaml

# class Start(Base_gns):
#     def __init__(self):
#         super().__init__()


    
    

if __name__=="__main__":
    current_lab = Base_gns()
    print(current_lab.start_nodes_from_project())
    print(current_lab.name_lab)