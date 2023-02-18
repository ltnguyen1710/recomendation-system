from pathlib import Path
import pandas as pd

# ------------------------Import Package DATABASE------------------------
import sys
sys.path.insert(0, 'DATABASE')
from DTB_dataset import DTB_dataset


class CONTROL_import:
    def __init__(self):
        self.dtb = DTB_dataset()
        pass

    def add_data(self,tb_name,df):     
        # Khởi tạo bảng
        table_name = tb_name
        list_col = list(df.columns)
        for i in list_col:
            if pd.api.types.is_numeric_dtype(df[i].dtypes):
                df[i] = df[i].fillna(0)
            else:
                df[i] = df[i].fillna('')
        state_create_table = self.dtb.create_table(table_name,list_col)
        
        if(state_create_table==True):    
            # Update data vào bảng
            state_update_table = self.dtb.update_table(table_name,df)
            if(state_update_table==True):
                self.alert = "Your file has been imported successfully!!!"
            else:
                self.alert = "ERROR: \n"+ "something went wrong"
        else:
            self.alert = "ERROR: \n"+"something went wrong"
        
    def show_alert(self):
        return self.alert
        
        

