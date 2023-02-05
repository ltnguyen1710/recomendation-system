import myfm
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from myfm.utils.benchmark_data import MovieLens100kDataManager
from sklearn.preprocessing import MultiLabelBinarizer, OneHotEncoder
import scipy.sparse as sps
from itertools import combinations
import numpy as np


class CONTROL_Statistical_Normalization:
    def __init__(self):
        pass

        # change columns of pandas to true datatype
    def change_to_true_dtype(self, data: pd.DataFrame):
        for i in data.columns:
            try:
                data[i] = pd.to_numeric(data[i])
            except ValueError:
                data[i] = data[i].astype('object')
        return data

    # sort value of array
    def sort_array(self, array):
        if array == 'nan' or array == 'NaN' or pd.isna(array):
            return 'NaN'
        new_array = [i['name'] for i in eval(array)]
        new_array.sort()
        return new_array

    # check if value of column is dict
    def check_value_is_dict(self, data: pd.DataFrame, column: str):
        for i in range(data[column].values.shape[0]):
            try:
                if type(eval(data[column][i])) == dict:
                    return True 
            except:
                return False
        return False

    # check if value of column is list
    def check_value_is_list(self, data: pd.DataFrame, column: str):
        for i in range(data[column].values.shape[0]):
            try:
                if type(eval(data[column][i])) == list:
                    return True
            except:
                return False
        return False

    # prepare data for predict
    def prepare(self, data: pd.DataFrame):
        data = self.change_to_true_dtype(data)
        for i in data.columns:
            if 'id' in i:
                data.drop(columns=[i], axis=1, inplace=True)
                continue
            if 'id' not in i:
                if 'date' in i:
                    data[i] = pd.to_datetime(data[i])
                    # data[i] = [
                    #     str(x) for x in data[i].dt.year.fillna('NaN')]
                    data[i] = data[i].fillna('NaN')
                    continue
                if pd.api.types.is_numeric_dtype(data[i].dtypes) and 'rating' not in i and data[i].dtypes not in [np.dtype('bool')]:
                    data[i] = data[i].fillna(0)
                    # data[i] = data[i] // 5 * 5
                    continue
                if self.check_value_is_dict(data, i):
                    data[i] = data[i].fillna('NaN')
                    data[i] = data[i].apply(lambda x: 'NaN' if (
                        x == 'nan' or x == 'NaN') else eval(str(x))['name'])
                    continue
                if self.check_value_is_list(data, i):
                    data[i] = data[i].fillna('NaN')
                    data[i] = data[i].apply(lambda x: self.sort_array(x))
                    data[i] = data[i].apply(lambda x: 'NaN' if (
                        x == 'nan' or x == 'NaN') else '|'.join(
                        [i.replace(" ", "") for i in x]))
                    continue
        return data.copy()

    def label_for_non_date_dtype(self, df: pd.DataFrame):
        for column in df.columns.values:
            print(column)
            if (pd.api.types.is_numeric_dtype(df[column].dtypes) == False or df[column].dtypes in [np.dtype('bool')]) and 'date' not in column:
                uniqe_value = df[column].unique()
                print(uniqe_value)
                print(len(uniqe_value))
                if len(uniqe_value) >= int(df.values.shape[0]*0.8):
                    df.drop(columns=[column], inplace=True)
                    continue
                new_value = {uniqe_value[i]: i+1 for i in range(len(uniqe_value))}
                # df[[column]] = df[[column]].replace(uniqe_value,[i for i in range(len(uniqe_value))])
                df[[column]] = df[[column]].replace(new_value)

        return df

    def new_date(self, x, new_realease_day):
        for i in range(new_realease_day.index.shape[0]-1):
            if new_realease_day.index[i] < x <= new_realease_day.index[i+1]:
                return new_realease_day.index[i+1]

    def label_for_date_dtype(self, df: pd.DataFrame):
        for i in df.columns:
            if 'date' in i:
                date_label = str(i)
        df[date_label] = pd.to_datetime(df[date_label],infer_datetime_format=True)
        new_realease_day = df.resample('9M', on=date_label).count()

        indexDate = new_realease_day[(
            new_realease_day[date_label] == 0)].index
        new_realease_day.drop(indexDate, inplace=True)

        for i in range(new_realease_day.index.shape[0]-1):
            df[date_label] = df[date_label].apply(lambda x: new_realease_day.index[i+1] if (
                new_realease_day.index[i] < x <= new_realease_day.index[i+1]) else x)
        unique_value = df[date_label].unique()
        new_value = {unique_value[i]: i+1 for i in range(len(unique_value))}
        df[date_label] = df[date_label].replace(new_value)
        return df

    def calculate_correof(self, df_corr):
        df_corr = df_corr.astype('float')
        self.corrcoef = df_corr.corr()

    def rank(self, column):
        return self.corrcoef.sort_values(by=[column], ascending=False)[column]
