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


class CONTROL_normalization:
    def __init__(self):
        self.minRMSE = float('inf')
        self.bestfeature_user = []
        self.bestfeature_movie = []
        self.myfm = myfm.MyFMGibbsRegressor(rank=10, random_seed=42,)

    def normalize_data(self, data_normalized: pd.DataFrame):
        if 'movie_release_date' in data_normalized.columns:
            data_normalized['movie_release_date'] = pd.to_datetime(
                data_normalized.movie_release_date)
            data_normalized['movie_release_year'] = [
                str(x) for x in data_normalized['movie_release_date'].dt.year.fillna('NaN')]
        if "user_age" in data_normalized.columns:
            data_normalized["user_age"] = data_normalized.user_age.astype(int) // 5 * 5
        if "user_zipcode" in data_normalized.columns:
            data_normalized["user_zipcode"] = data_normalized.user_zipcode.str[0]
        return data_normalized.copy()

    def train(self, data_normalized: pd.DataFrame):
        data_normalized = self.normalize_data(data_normalized)
        FEATURE_COLUMNS = ['user_id', 'movie_id']
        ohe = OneHotEncoder(handle_unknown='ignore')
        df_train = data_normalized[:int(len(data_normalized.values)*0.8)]
        X_train = ohe.fit_transform(
            df_train[FEATURE_COLUMNS])
        y_train = df_train.rating.values
        # user features
        user_feature_name = [
            col for col in data_normalized.columns if 'user' in col]
        user_data = data_normalized[user_feature_name].drop_duplicates(
            subset="user_id").set_index('user_id')
        current_user_Data_ohe = OneHotEncoder(
            handle_unknown='ignore').fit(user_data)

        # movie features
        movie_feature_name = [
            col for col in data_normalized.columns if 'movie' in col and 'movie_release_date' not in col]
        movie_data = data_normalized[movie_feature_name].drop_duplicates(
            subset="movie_id").set_index('movie_id')
        current_movie_Data_ohe = OneHotEncoder(
            handle_unknown='ignore').fit(movie_data)

        if 'movie_genres' in movie_feature_name:
            movie_genre = movie_data.loc[:, ['movie_genres']]
            movie_genre_mle = MultiLabelBinarizer(sparse_output=True).fit(
                movie_genre.movie_genres.apply(lambda x: x.split('|'))
            )
            X_train_extended = sps.hstack([
                X_train,
                current_user_Data_ohe.transform(
                    user_data.reindex(df_train.user_id)
                ),
                current_movie_Data_ohe.transform(
                    movie_data.reindex(
                        df_train.movie_id)
                ),
                movie_genre_mle.transform(
                    movie_genre.movie_genres.reindex(
                        df_train.movie_id).apply(lambda x: x.split('|'))
                )
            ])
            group_shapes_extended = (
                [len(group) for group in ohe.categories_] +
                [len(group) for group in current_user_Data_ohe.categories_] +
                [len(group) for group in current_movie_Data_ohe.categories_] +
                [len(movie_genre_mle.classes_)]
            )
            print(group_shapes_extended)
        else:
            X_train_extended = sps.hstack([
                X_train,
                current_user_Data_ohe.transform(
                    user_data.reindex(df_train.user_id)
                ),
                current_movie_Data_ohe.transform(
                    movie_data.reindex(
                        df_train.movie_id)
                ),
            ])
            group_shapes_extended = (
                [len(group) for group in ohe.categories_] +
                [len(group) for group in current_user_Data_ohe.categories_] +
                [len(group) for group in current_movie_Data_ohe.categories_]
            )
        self.myfm.fit(X_train_extended, y_train, n_iter=150, n_kept_samples=150,
                      group_shapes=group_shapes_extended)

    def prepare_for_predict(self, user_vs_movie: pd.DataFrame, data_normalized: pd.DataFrame):
        user_vs_movie = self.normalize_data(user_vs_movie)
        data_normalized = self.normalize_data(data_normalized)
        FEATURE_COLUMNS = ['user_id', 'movie_id']
        ohe = OneHotEncoder(handle_unknown='ignore')
        df_train = data_normalized[:int(len(data_normalized.values)*0.8)]
        ohe.fit_transform(df_train[FEATURE_COLUMNS])
        X_test = ohe.transform(user_vs_movie[FEATURE_COLUMNS])
        # user features
        user_feature_name = [
            col for col in data_normalized.columns if 'user' in col]
        user_data = data_normalized[user_feature_name].drop_duplicates(
            subset="user_id").set_index('user_id')
        current_user_Data_ohe = OneHotEncoder(
            handle_unknown='ignore').fit(user_data)

        # movie features
        movie_feature_name = [
            col for col in data_normalized.columns if 'movie' in col and 'movie_release_date' not in col]
        movie_data = data_normalized[movie_feature_name].drop_duplicates(
            subset="movie_id").set_index('movie_id')

        movie_genre = movie_data.loc[:, ['movie_genres']]
        current_movie_Data_ohe = OneHotEncoder(
            handle_unknown='ignore').fit(movie_data)
        movie_genre_mle = MultiLabelBinarizer(sparse_output=True).fit(
            movie_genre.movie_genres.apply(lambda x: x.split('|'))
        )

        X_test_extended = sps.hstack([
            X_test,
            current_user_Data_ohe.transform(
                user_data.reindex(user_vs_movie.user_id)
            ),
            current_movie_Data_ohe.transform(
                movie_data.reindex(
                    user_vs_movie.movie_id)
            ),
            movie_genre_mle.transform(
                movie_genre.movie_genres.reindex(
                    user_vs_movie.movie_id).apply(lambda x: x.split('|'))
            )
        ])
        group_shapes_extended = (
            [len(group) for group in ohe.categories_] +
            [len(group) for group in current_user_Data_ohe.categories_] +
            [len(group) for group in current_movie_Data_ohe.categories_] +
            [len(movie_genre_mle.classes_)]
        )
        print(group_shapes_extended)
        return X_test_extended

    def full_feature_rmse(
            self,
            full_dataset: pd.DataFrame,
            df_train: pd.DataFrame,
            df_test: pd.DataFrame):

        full_dataset = self.normalize_data(full_dataset)

        FEATURE_COLUMNS = ['user_id', 'movie_id']

        ohe = OneHotEncoder(handle_unknown='ignore')

        X_train = ohe.fit_transform(df_train[FEATURE_COLUMNS])
        X_test = ohe.transform(df_test[FEATURE_COLUMNS])
        y_train = df_train.rating.values
        y_test = df_test.rating.values

        user_feature_name = [
            col for col in full_dataset.columns if 'user' in col]
        user_info = full_dataset[user_feature_name].drop_duplicates(
            subset="user_id").set_index('user_id')
        user_info_ohe = OneHotEncoder(handle_unknown='ignore').fit(user_info)

        movie_feature_name = [
            col for col in full_dataset.columns if 'movie' in col]
        movie_info = full_dataset[movie_feature_name].drop_duplicates(
            subset="movie_id").set_index('movie_id')
        movie_info = movie_info[['movie_release_year', 'movie_genres']]
        movie_info_ohe = OneHotEncoder(handle_unknown='ignore').fit(
            movie_info[['movie_release_year']])
        movie_genre_mle = MultiLabelBinarizer(sparse_output=True).fit(
            movie_info.movie_genres.apply(lambda x: x.split('|'))
        )

        X_train_extended = sps.hstack([
            X_train,
            user_info_ohe.transform(
                user_info.reindex(df_train.user_id)
            ),
            movie_info_ohe.transform(
                movie_info.reindex(df_train.movie_id).drop(
                    columns=['movie_genres'])
            ),
            movie_genre_mle.transform(
                movie_info.movie_genres.reindex(
                    df_train.movie_id).apply(lambda x: x.split('|'))
            )
        ])

        X_test_extended = sps.hstack([
            X_test,
            user_info_ohe.transform(
                user_info.reindex(df_test.user_id)
            ),
            movie_info_ohe.transform(
                movie_info.reindex(df_test.movie_id).drop(
                    columns=['movie_genres'])
            ),
            movie_genre_mle.transform(
                movie_info.movie_genres.reindex(
                    df_test.movie_id).apply(lambda x: x.split('|'))
            )
        ])

        group_shapes_extended = (
            [len(group) for group in ohe.categories_] +
            [len(group) for group in user_info_ohe.categories_] +
            [len(group) for group in movie_info_ohe.categories_] +
            [len(movie_genre_mle.classes_)]
        )
        print(group_shapes_extended)
        fm_side_info = myfm.MyFMRegressor(
            rank=10, random_seed=42,
        )
        fm_side_info.fit(
            X_train_extended, y_train, n_iter=150, n_kept_samples=150,
            group_shapes=group_shapes_extended
        )

        prediction_side_info = fm_side_info.predict(X_test_extended)
        rmse = ((y_test - prediction_side_info) ** 2).mean() ** .5
        # mae = np.abs(y_test - prediction_side_info).mean()
        print(f'rmse={rmse}')
        return rmse
    # function to generate all the sub lists

    def sub_lists(self, l):
        # initializing empty list
        comb = []

        # Iterating till length of list
        for i in range(len(l)+1):
            # Generating sub list
            comb += [list(j) for j in combinations(l, i)]
        # Returning list
        return comb

    # function to get best features of dataset
    def best_features(
            self,
            full_dataset: pd.DataFrame,
            df_train: pd.DataFrame,
            df_test: pd.DataFrame,
            full_feature_rmse=float('inf')):
        full_dataset = self.normalize_data(full_dataset)
        ohe = OneHotEncoder(handle_unknown='ignore')
        FEATURE_COLUMNS = ['user_id', 'movie_id']
        X_train = ohe.fit_transform(df_train[FEATURE_COLUMNS])
        X_test = ohe.transform(df_test[FEATURE_COLUMNS])
        y_train = df_train.rating.values
        y_test = df_test.rating.values
        # user features
        user_feature_name = [
            col for col in full_dataset.columns if 'user' in col]
        user_data = full_dataset[user_feature_name].drop_duplicates(
            subset="user_id").set_index('user_id')
        sub_lists_user = self.sub_lists(user_data.columns)
        # movie features
        movie_feature_name = [
            col for col in full_dataset.columns if 'movie' in col]
        movie_data = full_dataset[movie_feature_name].drop_duplicates(
            subset="movie_id").set_index('movie_id')
        movie_data = movie_data[['movie_release_year', 'movie_genres']]
        sub_list_movie = self.sub_lists(movie_data.columns)

        minRMSE = full_feature_rmse
        bestfeature_movie = []
        bestfeature_user = []

        for i in sub_list_movie:
            if len(i) > 0:
                if 'movie_genres' not in i:
                    print(i)
                    current_movie_Data = movie_data.loc[:, i]
                    current_movie_Data_ohe = OneHotEncoder(
                        handle_unknown='ignore').fit(current_movie_Data)
                    for j in sub_lists_user:
                        if len(j) > 0:
                            current_user_Data = user_data.loc[:, j]
                            current_user_Data_ohe = OneHotEncoder(
                                handle_unknown='ignore').fit(current_user_Data)
                            X_train_extended = sps.hstack([
                                X_train,
                                current_user_Data_ohe.transform(
                                    current_user_Data.reindex(df_train.user_id)
                                ),
                                current_movie_Data_ohe.transform(
                                    current_movie_Data.reindex(
                                        df_train.movie_id)
                                ),
                            ])

                            X_test_extended = sps.hstack([
                                X_test,
                                current_user_Data_ohe.transform(
                                    current_user_Data.reindex(df_test.user_id)
                                ),
                                current_movie_Data_ohe.transform(
                                    current_movie_Data.reindex(
                                        df_test.movie_id)
                                ),
                            ])
                            group_shapes_extended = (
                                [len(group) for group in ohe.categories_] +
                                [len(group) for group in current_user_Data_ohe.categories_] +
                                [len(group)
                                 for group in current_movie_Data_ohe.categories_]
                            )
                            print(group_shapes_extended)
                            fm_side_info = myfm.MyFMRegressor(
                                rank=10, random_seed=42,
                            )
                            fm_side_info.fit(
                                X_train_extended, y_train, n_iter=150, n_kept_samples=150,
                                group_shapes=group_shapes_extended
                            )

                            prediction_side_info = fm_side_info.predict(
                                X_test_extended)
                            rmse = ((y_test - prediction_side_info)
                                    ** 2).mean() ** .5
                            # mae = np.abs(y_test - prediction_side_info).mean()
                            print(f'rmse={rmse}')
                            if minRMSE > rmse:
                                minRMSE = rmse
                                bestfeature_user = j
                                bestfeature_movie = i
                                break
                else:
                    current_movie_Data = movie_data.loc[:, i].drop(
                        columns=['movie_genres'])
                    movie_genre = movie_data.loc[:, ['movie_genres']]
                    current_movie_Data_ohe = OneHotEncoder(
                        handle_unknown='ignore').fit(current_movie_Data)
                    print(i)
                    movie_genre_mle = MultiLabelBinarizer(sparse_output=True).fit(
                        movie_genre.movie_genres.apply(lambda x: x.split('|'))
                    )
                    for j in sub_lists_user:
                        if len(j) > 0:
                            current_user_Data = user_data.loc[:, j]
                            current_user_Data_ohe = OneHotEncoder(
                                handle_unknown='ignore').fit(current_user_Data)
                            X_train_extended = sps.hstack([
                                X_train,
                                current_user_Data_ohe.transform(
                                    current_user_Data.reindex(df_train.user_id)
                                ),
                                current_movie_Data_ohe.transform(
                                    current_movie_Data.reindex(
                                        df_train.movie_id)
                                ),
                                movie_genre_mle.transform(
                                    movie_genre.movie_genres.reindex(
                                        df_train.movie_id).apply(lambda x: x.split('|'))
                                )
                            ])

                            X_test_extended = sps.hstack([
                                X_test,
                                current_user_Data_ohe.transform(
                                    current_user_Data.reindex(df_test.user_id)
                                ),
                                current_movie_Data_ohe.transform(
                                    current_movie_Data.reindex(
                                        df_test.movie_id)
                                ),
                                movie_genre_mle.transform(
                                    movie_genre.movie_genres.reindex(
                                        df_test.movie_id).apply(lambda x: x.split('|'))
                                )
                            ])
                            group_shapes_extended = (
                                [len(group) for group in ohe.categories_] +
                                [len(group) for group in current_user_Data_ohe.categories_] +
                                [len(group) for group in current_movie_Data_ohe.categories_] +
                                [len(movie_genre_mle.classes_)]
                            )
                            print(group_shapes_extended)
                            fm_side_info = myfm.MyFMRegressor(
                                rank=10, random_seed=42,
                            )
                            fm_side_info.fit(
                                X_train_extended, y_train, n_iter=150, n_kept_samples=150,
                                group_shapes=group_shapes_extended
                            )

                            prediction_side_info = fm_side_info.predict(
                                X_test_extended)
                            rmse = ((y_test - prediction_side_info)
                                    ** 2).mean() ** .5
                            # mae = np.abs(y_test - prediction_side_info).mean()
                            print(f'rmse={rmse}')
                            if minRMSE > rmse:
                                minRMSE = rmse
                                bestfeature_user = j
                                bestfeature_movie = i
                                break

        self.minRMSE = minRMSE
        self.bestfeature_user = bestfeature_user
        self.bestfeature_movie = bestfeature_movie
        return (minRMSE, bestfeature_user, bestfeature_movie)

    def new_dataset(self, df_train_tosave: pd.DataFrame, df_test_tosave: pd.DataFrame):
        datatosave = pd.concat(
            [df_train_tosave, df_test_tosave]).reset_index().drop(columns=['index'])
        new_features = ['user_id', 'movie_id', 'rating'] + \
            self.bestfeature_user + self.bestfeature_movie
        for i in range(len(new_features)):
            if new_features[i] == 'movie_release_year':
                new_features[i] = 'movie_release_date'
                break
        newData = datatosave.loc[:, new_features]
        return newData

    def merge_user_vs_movie(self, user_info, movie_info):
        user_vs_movie = pd.concat([user_info, movie_info], axis=1)
        return user_vs_movie


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
# full_feature_dataset = result.copy()
# df_train, df_test = train_test_split(full_feature_dataset, test_size=0.2)
# df_train_tosave = df_train.copy()
# df_test_tosave = df_test.copy()

# normalization = CONTROL_normalization()
# # full_feature_rmse = normalization.full_feature_rmse(full_feature_dataset, df_train, df_test)
# normalization.best_features(full_feature_dataset, df_train, df_test, )
# print(normalization.minRMSE)
# print(normalization.bestfeature_user)
# print(normalization.bestfeature_movie)
# print(normalization.new_dataset(df_train_tosave, df_test_tosave))
# # print(result)
