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
from movie import movie
from CONTROL_normalization import CONTROL_normalization

class user:
    def __init__(self):
        pass

    def get_user_info(self, dataset: pd.DataFrame):
        user_feature_name = [col for col in dataset.columns if 'user' in col]
        user_data = dataset[user_feature_name].drop_duplicates(
            subset="user_id").sort_values(by='user_id').reset_index().drop(columns=["index"])
        self.user_data = user_data.copy()
        return user_data

    def get_user_info_by_id(self, id: int):
        self.user_info = self.user_data[self.user_data.user_id == id]
        return self.user_info.copy().reset_index().drop(columns=["index"])


# data_manager = MovieLens100kDataManager()

# # print(dataset.load_rating_predefined_split(3))
# ratings = data_manager.load_rating_all().drop(columns=['timestamp'])
# users = data_manager.load_user_info()
# columns_users = []
# for col in users.columns:
#     if str(col) != 'user_id':
#         columns_users.append('user_'+str(col))
#     else:
#         columns_users.append(str(col))
# users = pd.DataFrame(users.values, columns=columns_users)
# # Merge tập ratings và users được gom nhóm bởi user_id
# result = pd.merge(ratings, users, on="user_id", how="outer")

# movies = data_manager.load_movie_info()
# columns_movies = []
# for col in movies[['movie_id', 'release_date', 'genres']].columns:
#     if str(col) != 'movie_id':
#         columns_movies.append('movie_'+str(col))
#     else:
#         columns_movies.append(str(col))
# movies = pd.DataFrame(
#     movies[['movie_id', 'release_date', 'genres']].values, columns=columns_movies)
# result = pd.merge(result, movies, on="movie_id", how="outer")
# # print(result.loc[:int(len(result.values)*0.8),['movie_id']])
# normalize = CONTROL_normalization()
# normalize.train(result)

# users = user()
# movies = movie()
# print(users.get_user_info(result))
# user_info = users.get_user_info_by_id(368)
# print(movies.get_movie_info(result))
# movie_info = movies.get_movie_info_by_id(441)
# # user_vs_movie = pd.concat([user_info, movie_info], axis=1)
# # print(user_vs_movie.columns)
# user_vs_movie = normalize.merge_user_vs_movie(user_info,movie_info)
# print(user_vs_movie)
# X_test = normalize.prepare_for_predict(user_vs_movie,result)
# print(X_test)
# print(normalize.myfm.predict(X_test))


# user_vs_movie['movie_release_year'] = [
# str(x) for x in user_vs_movie['movie_release_date'].dt.year.fillna('NaN')]
# user_vs_movie["user_age"] = user_vs_movie.user_age // 5 * 5
# user_vs_movie["user_zipcode"] = user_vs_movie.user_zipcode.str[0]
# FEATURE_COLUMNS = ['user_id', 'movie_id']
# ohe = OneHotEncoder(handle_unknown='ignore')
# X_test = ohe.fit_transform(user_vs_movie[FEATURE_COLUMNS])
# # user features
# user_feature_name = [
#     col for col in user_vs_movie.columns if 'user' in col]
# user_data = user_vs_movie[user_feature_name].drop_duplicates(
#     subset="user_id").set_index('user_id')

# # movie features
# movie_feature_name = [
#     col for col in user_vs_movie.columns if 'movie' in col and 'movie_release_date' not in col]
# print(movie_feature_name)
# movie_data = user_vs_movie[movie_feature_name].drop_duplicates(
#     subset="movie_id").set_index('movie_id')

# current_user_Data_ohe = OneHotEncoder(
#     handle_unknown='ignore').fit(user_data)

# movie_genre = movie_data.loc[:, ['movie_genres']]
# current_movie_Data_ohe = OneHotEncoder(
#     handle_unknown='ignore').fit(movie_data)
# movie_genre_mle = MultiLabelBinarizer(sparse_output=True).fit(
#     movie_genre.movie_genres.apply(lambda x: x.split('|'))
# )

# X_test_extended = sps.hstack([
#     X_test,
#     current_user_Data_ohe.transform(
#         user_data.reindex(user_vs_movie.user_id)
#     ),
#     current_movie_Data_ohe.transform(
#         movie_data.reindex(
#             user_vs_movie.movie_id)
#     ),
#     movie_genre_mle.transform(
#         movie_genre.movie_genres.reindex(
#             user_vs_movie.movie_id).apply(lambda x: x.split('|'))
#     )
# ])
# group_shapes_extended = (
#     [len(group) for group in ohe.categories_] +
#     [len(group) for group in current_user_Data_ohe.categories_] +
#     [len(group) for group in current_movie_Data_ohe.categories_]
# )
# print(group_shapes_extended)

