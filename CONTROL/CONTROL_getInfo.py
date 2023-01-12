from pathlib import Path
import pandas as pd

# ------------------------Import Package DATABASE------------------------
import sys
sys.path.insert(0, 'DATABASE')
from DTB_dataset import DTB_dataset

class CONTROL_getInfo:
    def __init__(self):
        self.dtb = DTB_dataset()
        

    def get_list_Table(self):
        return self.dtb.get_list_Table()

    
        
        

