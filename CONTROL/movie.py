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


class movie:
    def __init__(self):
        pass

    def get_movie_info(self, dataset: pd.DataFrame):
        movie_feature_name = [col for col in dataset.columns if 'movie' in col]
        movie_data = dataset[movie_feature_name].drop_duplicates(
            subset="movie_id").sort_values(by='movie_id').reset_index().drop(columns=["index"])
        self.movie_data = movie_data.copy()
        return movie_data

    def get_movie_info_by_id(self, id: int):
        self.movie_info = self.movie_data[self.movie_data.movie_id == id]
        return self.movie_info.copy().reset_index().drop(columns=["index"])
