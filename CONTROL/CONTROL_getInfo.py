from pathlib import Path
import pandas as pd
from user import user
from movie import movie

# ------------------------Import Package DATABASE------------------------
import sys
sys.path.insert(0, 'DATABASE')
from DTB_dataset import DTB_dataset


# change columns of pandas to true datatype


def change_to_true_dtype(data: pd.DataFrame):
    for i in data.columns:
        try:
            data[i] = pd.to_numeric(data[i])
        except ValueError:
            data[i] = data[i].astype('object')
    return data

# sort value of array


def sort_array(array):
    if array == 'nan' or array == 'NaN' or pd.isna(array):
        return 'NaN'
    new_array = [i['name'] for i in eval(array)]
    new_array.sort()
    return new_array

# check if value of column is dict


def check_value_is_dict(data: pd.DataFrame, column: str):
    for i in range(data[column].values.shape[0]):
        try:
            if type(eval(data[column][i])) == dict:
                return True
        except:
            return False
    return False

# check if value of column is list


def check_value_is_list(data: pd.DataFrame, column: str):
    for i in range(data[column].values.shape[0]):
        try:
            if type(eval(data[column][i])) == list:
                return True
        except:
            return False
    return False

# check value of column have multi label. For example: Action|Cartoon|Thriller


def check_multi_label(data: pd.DataFrame, column: str):
    try:
        result = data[column].str.contains('|', regex=False)
        # print(result.index)
        for i in result.index:
            # print(result[i])
            if result[i] == True:
                return True
    except:
        return False
    return False

# set array of multi label encoder to array of sparse matrix . For example: [mle, mle, mel] -> [matrix,matrix,matrix]


def multi_mle_to_multi_array(mle_list: list, column_list: list, df: pd.DataFrame):
    result = []
    for i in range(len(mle_list)):
        current_feature = column_list[i]
        current_column = current_feature.columns[0]
        array = mle_list[i].transform(current_feature[current_column].reindex(
            df['movie_id']).apply(lambda x: x.split('|')))
        result.append(array)
    return result

# prepare data for predict


def prepare(data: pd.DataFrame):
    data = change_to_true_dtype(data)
    for i in data.columns:
        if 'date' in i:
            data[i] = pd.to_datetime(data[i])
            data[i] = [
                str(x) for x in data[i].dt.year.fillna('NaN')]
            continue
        if pd.api.types.is_numeric_dtype(data[i].dtypes):
            data[i] = data[i].fillna(0)
            continue
        if check_value_is_dict(data, i):
            data[i] = data[i].fillna('NaN')
            data[i] = data[i].apply(lambda x: 'NaN' if (
                x == 'nan' or x == 'NaN') else eval(str(x))['name'])
            continue
        if check_value_is_list(data, i):
            data[i] = data[i].fillna('NaN')
            data[i] = data[i].apply(lambda x: sort_array(x))
            data[i] = data[i].apply(lambda x: 'NaN' if (
                x == 'nan' or x == 'NaN') else '|'.join(
                [i.replace(" ", "") for i in x]))
            continue
    return data.copy()

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

        return prepare(self.dtb.query_table(sql))

    def get_user_info(self,dataset):
        return self.user.get_user_info(dataset)

    def get_user_info_by_id(self,id):
        return self.user.get_user_info_by_id(id)

    def get_movie_info(self,dataset):
        return self.movie.get_movie_info(dataset)

    def get_movie_info_by_id(self,id):
        return self.movie.get_movie_info_by_id(id)

    
        
        

