from pathlib import Path
import pandas as pd
from user import user
from movie import movie

# ------------------------Import Package DATABASE------------------------
import sys
sys.path.insert(0, 'DATABASE')
from DTB_dataset import DTB_dataset

"""
Class này dùng để Lấy dữ liệu để dự đoán (Predict Movie)
"""
class CONTROL_getInfo:
    def __init__(self):
        self.dtb = DTB_dataset()
        self.user = user()
        self.movie = movie()
        

    def get_list_Table(self):
        return self.dtb.get_list_Table()

    def query_table(self,sql):
        return self.dtb.query_table(sql)

    def get_user_info(self,dataset):
        return self.user.get_user_info(dataset)

    def get_user_info_by_id(self,id):
        return self.user.get_user_info_by_id(id)

    def get_movie_info(self,dataset):
        return self.movie.get_movie_info(dataset)

    def get_movie_info_by_id(self,id):
        return self.movie.get_movie_info_by_id(id)

    
        
        

