import myfm
import pandas as pd
from myfm.utils.benchmark_data import MovieLens100kDataManager
from sklearn.preprocessing import MultiLabelBinarizer, OneHotEncoder
import scipy.sparse as sps


class CONTROL_recommendation:
    def __init__(self):
        self.myfm = myfm.MyFMGibbsRegressor(rank=10, random_seed=42,)

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

    # check value of column have multi label. For example: Action|Cartoon|Thriller
    def check_multi_label(self, data: pd.DataFrame, column: str):
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
    def multi_mle_to_multi_array(self,mle_list: list, column_list: list, df: pd.DataFrame):
        result = []
        for i in range(len(mle_list)):
            current_feature = column_list[i]
            current_column = current_feature.columns[0]
            array = mle_list[i].transform(current_feature[current_column].reindex(
                df['movie_id']).apply(lambda x: x.split('|')))
            result.append(array)
        return result

    # prepare data for predict
    def prepare(self, data: pd.DataFrame):
        data = self.change_to_true_dtype(data)
        for i in data.columns:
            if 'id' in i and i not in ['movie_id', 'user_id']:
                data.drop(columns=[i], axis=1, inplace=True)
                continue
            if 'id' not in i:
                if 'date' in i:
                    data[i] = pd.to_datetime(data[i])
                    data[i] = [
                        str(x) for x in data[i].dt.year.fillna('NaN')]
                    continue
                if pd.api.types.is_numeric_dtype(data[i].dtypes) and 'rating' not in i:
                    data[i] = data[i] // 5 * 5
                    continue
                if self.check_value_is_dict(data, i):
                    data[i] = data[i].apply(lambda x: 'NaN' if (
                        pd.isna(x)) else eval(str(x))['name'])
                    continue
                if self.check_value_is_list(data, i):
                    data[i] = data[i].apply(lambda x: self.sort_array(x))
                    data[i] = data[i].apply(lambda x: '|'.join(
                        [i.replace(" ", "") for i in x]))
                    continue
        return data.copy()

    def train(self, data: pd.DataFrame):
        data = self.prepare(data)
        FEATURE_COLUMNS = ['user_id', 'movie_id']
        ohe = OneHotEncoder(handle_unknown='ignore')
        df_train = data
        X_train = ohe.fit_transform(
            df_train[FEATURE_COLUMNS])
        y_train = df_train.rating.values
        # user features
        user_feature_name = [
            col for col in data.columns if 'user' in col]
        user_data = data[user_feature_name].drop_duplicates(
            subset="user_id").set_index('user_id')
        user_multi_label_list = []
        user_multi_label_mle_list = []
        for i in user_data.columns.values:
            if self.check_multi_label(user_data, i):
                column = user_data.loc[:, [i]]
                column_mle = MultiLabelBinarizer(sparse_output=True).fit(
                    column[i].apply(lambda x: x.split('|'))
                )
                user_multi_label_list.append(column)
                user_multi_label_mle_list.append(column_mle)
                user_data.drop(columns=[i], axis=1, inplace=True)
        current_user_Data_ohe = OneHotEncoder(
            handle_unknown='ignore').fit(user_data)

        # movie features
        movie_feature_name = [
            col for col in data.columns if 'movie' in col]
        movie_data = data[movie_feature_name].drop_duplicates(
            subset="movie_id").set_index('movie_id')
        movie_multi_label_list = []
        movie_multi_label_mle_list = []
        for i in movie_data.columns.values:
            if self.check_multi_label(movie_data, i):
                column = movie_data.loc[:, [i]]
                column_mle = MultiLabelBinarizer(sparse_output=True).fit(
                    column[i].apply(lambda x: x.split('|'))
                )
                movie_multi_label_list.append(column)
                movie_multi_label_mle_list.append(column_mle)
                movie_data.drop(columns=[i], axis=1, inplace=True)
        current_movie_Data_ohe = OneHotEncoder(
            handle_unknown='ignore').fit(movie_data)

        # print(user_multi_label_list)
        # print(user_multi_label_mle_list)
        # print(movie_multi_label_list[0])
        # print(movie_multi_label_mle_list)
        # print(multi_mle_to_multi_array(movie_multi_label_mle_list,movie_multi_label_list,df_train))
        user_multi_label_mle_array = self.multi_mle_to_multi_array(
            user_multi_label_mle_list, user_multi_label_list, df_train)
        movie_multi_label_mle_array = self.multi_mle_to_multi_array(
            movie_multi_label_mle_list, movie_multi_label_list, df_train)
        X_train_extended = sps.hstack([
            X_train,
            current_user_Data_ohe.transform(
                user_data.reindex(df_train.user_id)
            ),
            current_movie_Data_ohe.transform(
                movie_data.reindex(
                    df_train.movie_id)
            ),
            *user_multi_label_mle_array,
            *movie_multi_label_mle_array
            # movie_genre_mle.transform(
            #     movie_genre.movie_genres.reindex(
            #         df_train.movie_id).apply(lambda x: x.split('|'))
            # )
        ])
        group_shapes_extended = (
            [len(group) for group in ohe.categories_] +
            [len(group) for group in current_user_Data_ohe.categories_] +
            [len(group) for group in current_movie_Data_ohe.categories_]
            # [len(movie_genre_mle.classes_)]
        )
        for i in range(len(user_multi_label_mle_list)):
            current = user_multi_label_mle_list[i]
            group_shapes_extended = group_shapes_extended + \
                [len(current.classes_)]

        for i in range(len(movie_multi_label_mle_list)):
            current = movie_multi_label_mle_list[i]
            group_shapes_extended = group_shapes_extended + \
                [len(current.classes_)]

        print(group_shapes_extended)
        self.myfm.fit(X_train_extended, y_train, n_iter=150, n_kept_samples=150,
                      group_shapes=group_shapes_extended)

    def prepare_for_predict(self, user_vs_movie: pd.DataFrame, data: pd.DataFrame):
        user_vs_movie = self.prepare(user_vs_movie)
        data = self.prepare(data)
        FEATURE_COLUMNS = ['user_id', 'movie_id']
        ohe = OneHotEncoder(handle_unknown='ignore')
        df_train = data
        ohe.fit_transform(df_train[FEATURE_COLUMNS])
        X_test = ohe.transform(user_vs_movie[FEATURE_COLUMNS])
        # user features
        user_feature_name = [
            col for col in data.columns if 'user' in col]
        user_data = data[user_feature_name].drop_duplicates(
            subset="user_id").set_index('user_id')
        user_multi_label_list = []
        user_multi_label_mle_list = []
        for i in user_data.columns.values:
            if self.check_multi_label(user_data, i):
                column = user_data.loc[:, [i]]
                column_mle = MultiLabelBinarizer(sparse_output=True).fit(
                    column[i].apply(lambda x: x.split('|'))
                )
                user_multi_label_list.append(column)
                user_multi_label_mle_list.append(column_mle)
                user_data.drop(columns=[i], axis=1, inplace=True)
        current_user_Data_ohe = OneHotEncoder(
            handle_unknown='ignore').fit(user_data)

        # movie features
        movie_feature_name = [
            col for col in data.columns if 'movie' in col]
        movie_data = data[movie_feature_name].drop_duplicates(
            subset="movie_id").set_index('movie_id')
        movie_multi_label_list = []
        movie_multi_label_mle_list = []
        for i in movie_data.columns.values:
            if self.check_multi_label(movie_data, i):
                column = movie_data.loc[:, [i]]
                column_mle = MultiLabelBinarizer(sparse_output=True).fit(
                    column[i].apply(lambda x: x.split('|'))
                )
                movie_multi_label_list.append(column)
                movie_multi_label_mle_list.append(column_mle)
                movie_data.drop(columns=[i], axis=1, inplace=True)
        current_movie_Data_ohe = OneHotEncoder(
            handle_unknown='ignore').fit(movie_data)

        user_multi_label_mle_array = self.multi_mle_to_multi_array(
            user_multi_label_mle_list, user_multi_label_list, user_vs_movie)
        movie_multi_label_mle_array = self.multi_mle_to_multi_array(
            movie_multi_label_mle_list, movie_multi_label_list, user_vs_movie)

        X_test_extended = sps.hstack([
            X_test,
            current_user_Data_ohe.transform(
                user_data.reindex(user_vs_movie.user_id)
            ),
            current_movie_Data_ohe.transform(
                movie_data.reindex(
                    user_vs_movie.movie_id)
            ),
            *user_multi_label_mle_array,
            *movie_multi_label_mle_array
            # movie_genre_mle.transform(
            #     movie_genre.movie_genres.reindex(
            #         user_vs_movie.movie_id).apply(lambda x: x.split('|'))
            # )
        ])
        group_shapes_extended = (
            [len(group) for group in ohe.categories_] +
            [len(group) for group in current_user_Data_ohe.categories_] +
            [len(group) for group in current_movie_Data_ohe.categories_]
        )
        for i in range(len(user_multi_label_mle_list)):
            current = user_multi_label_mle_list[i]
            group_shapes_extended = group_shapes_extended + \
                [len(current.classes_)]

        for i in range(len(movie_multi_label_mle_list)):
            current = movie_multi_label_mle_list[i]
            group_shapes_extended = group_shapes_extended + \
                [len(current.classes_)]
        print(group_shapes_extended)
        return X_test_extended

    #merge user info with unseen movie info
    def merge_user_vs_movie(self, user_info, unseen_movie_info):
        for i in range(unseen_movie_info.values.shape[0]-1):
            user_info.loc[len(user_info.index)] = user_info.loc[0]
        user_vs_movie = pd.concat([user_info, unseen_movie_info], axis=1,copy=True,)
        return user_vs_movie


