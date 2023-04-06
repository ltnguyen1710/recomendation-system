import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances, manhattan_distances
from scipy.stats import pearsonr
from scipy import sparse
from itertools import product
from BERT import BERT

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


class CF(object):
    """docstring for CF"""

    def __init__(self, Y_data: pd.DataFrame, k=0, dist_func=cosine_similarity, uuCF=1, bert=1):
      # cosine_similarity
      # euclidean_distances
      # manhattan_distances
        self.bert = bert
        self.Y_data_df = Y_data
        rating_data = Y_data.loc[:, ['user_id', 'movie_id', 'rating', ]].values
        self.uuCF = uuCF  # user-user (1) or item-item (0) CF
        self.Y_data = rating_data.astype(
            int) if uuCF else rating_data[:, [1, 0, 2]].astype(int)
        if bert:
            self.prepare_for_bert()
        self.k = k
        self.dist_func = dist_func
        self.Ybar_data = None
        # number of users and items. Remember to add 1 since id starts from 0
        # value biggest in arr - last user->number of user
        self.n_users = int(np.max(self.Y_data[:, 0])) + 1
        # value biggest in arr - last items->number of items
        self.n_items = int(np.max(self.Y_data[:, 1])) + 1
        self.rating_sparse = sparse.coo_matrix((np.array(self.Y_data[:, 2], dtype=float),
                                                (np.array(self.Y_data[:, 1], dtype=float), np.array(self.Y_data[:, 0], dtype=float))), (self.n_items, self.n_users))
        self.rating_sparse = self.rating_sparse.tocsr()
        self.rating_array = self.rating_sparse.toarray()

    def prepare_for_bert(self):
        self.bert_model = BERT()
        self.Y_data_df = prepare(self.Y_data_df)
        # plot_columns = self.Y_data_df.loc[:, self.Y_data_df.dtypes == object].columns
        # movie_features = self.Y_data_df.copy()
        # movie_features["merge"] = movie_features[[plot_columns]].agg(' '.join, axis=1)
        # movie_features = movie_features.drop_duplicates(
        #     subset="movie_id").sort_values(by='movie_id').reset_index().drop(columns=["index"])
        self.Y_data_df["merge"] = self.Y_data_df["title"] + ' ' + \
            self.Y_data_df["genres"]+' ' + \
            self.Y_data_df['overview'].fillna('')
        movie_features = self.Y_data_df.drop_duplicates(
            subset="movie_id").sort_values(by='movie_id').reset_index().drop(columns=["index"])
        self.merged_text = movie_features['merge'].values.tolist()

    def __update(self, new_data):
        users = new_data[:, 0]  # all users - first col of the Y_data
        Ybar_data = new_data.copy()  # copy new data

        firts_user = int(np.min(new_data[:, 0]))
        last_user = int(np.max(new_data[:, 0])) + 1
        # update mean array with new size
        if (last_user > np.size(self.mu)):
            new_size_mu = np.zeros((last_user-np.size(self.mu),))
            self.mu = np.append(self.mu, new_size_mu)
        # update n_user
        new_n_users = int(np.max(new_data[:, 0])) + 1
        if (self.n_users < new_n_users):
            self.n_users = new_n_users
        # update n_item
        new_n_items = int(np.max(new_data[:, 1])) + 1
        if (self.n_items < new_n_items):
            self.n_items = new_n_items

        for n in range(firts_user, last_user):
            # row indices of rating done by user n
            # since indices need to be integers, we need to convert
            ids = np.where(users == n)[0].astype(np.int32)
            # indices of all ratings associated with user n
            item_ids = new_data[ids, 1]
            # and the corresponding ratings
            ratings = new_data[ids, 2]
            # take mean (trung bình cộng)
            m = np.mean(ratings)
            # get Exeption if arr emty
            if np.isnan(m):
                m = 0  # to avoid empty array and nan value
            # mu is mean of rating by user n (or by istems n)
            self.mu[n] = m
            # normalize
            Ybar_data[ids, 2] = ratings - self.mu[n]
        ################################################
        # form the rating matrix as a sparse matrix. Sparsity is important
        # for both memory and computing efficiency. For example, if #user = 1M,
        # #item = 100k, then shape of the rating matrix would be (100k, 1M),
        # you may not have enough memory to store this. Then, instead, we store
        # nonzeros only, and, of course, their locations.

        Ybar = sparse.coo_matrix((Ybar_data[:, 2],
                                  (Ybar_data[:, 1], Ybar_data[:, 0])), (self.n_items, self.n_users))
        Ybar = Ybar.tocsr()
        self.Ybar = sparse.hstack((self.Ybar, Ybar), format='csr')

    def update(self, new_data):
        self.__update(new_data)
        self.similarity()

    def normalize_Y(self):
        users = self.Y_data[:, 0]  # all users - first col of the Y_data
        self.Ybar_data = self.Y_data.copy()  # copy new data
        # create arr 1D with '0', size n_users
        self.mu = np.zeros((self.n_users,))
        # Vòng for làm các bước:
        # b1: ép kiểu ids ->int32
        # ids là danh sách các item đã được rating của user thứ n
        # b2: Lấy tất cả item mà user đã rate
        # b3: Tính trung bình cộng các rating của user thứ n
        # b4: Bắt ngoại lệ nếu mảng rating emty
        # b5: lưu mean rating của user thứ n vào mảng
        # b6: Tính và lưu new_rating vào mảng vừa mới sao chép (Ybar_data)
        for n in range(self.n_users):
            # row indices of rating done by user n
            # since indices need to be integers, we need to convert
            ids = np.where(users == n)[0].astype(np.int32)
            # indices of all ratings associated with user n
            item_ids = self.Y_data[ids, 1]
            # and the corresponding ratings
            ratings = self.Y_data[ids, 2].astype(np.float32)
            # take mean (trung bình cộng)
            m = np.mean(ratings)
            # get Exeption if arr emty
            if np.isnan(m):
                m = 0  # to avoid empty array and nan value
            # mu is mean of rating by user n (or by istems n)
            self.mu[n] = m
            # normalize

            self.Ybar_data[ids, 2] = ratings - self.mu[n]

        ################################################
        # form the rating matrix as a sparse matrix. Sparsity is important
        # for both memory and computing efficiency. For example, if #user = 1M,
        # #item = 100k, then shape of the rating matrix would be (100k, 1M),
        # you may not have enough memory to store this. Then, instead, we store
        # nonzeros only, and, of course, their locations.

        self.Ybar = sparse.coo_matrix((np.array(self.Ybar_data[:, 2], dtype=float),
                                       (np.array(self.Ybar_data[:, 1], dtype=float), np.array(self.Ybar_data[:, 0], dtype=float))), (self.n_items, self.n_users))
        self.Ybar = self.Ybar.tocsr()

    def cal_user_embedding(self, user_item_ratings_matrix, item_bert_embedding_matrix):
        num_of_user = len(user_item_ratings_matrix[0])  # Get num of User
        # Get num of layer Item
        num_of_layer_item = len(item_bert_embedding_matrix)
        user_bert_embedding_matrix = np.zeros([num_of_layer_item, num_of_user])
        movie_id = self.Y_data_df['movie_id'].unique()
        for i in range(num_of_user):
            list_item_rate_by_user_i = np.array(self.list_item_rate_by_u(i))
            # print(list_item_rate_by_user_i)
            if len(list_item_rate_by_user_i) > 0:
                index = [i for i in range(
                    len(list_item_rate_by_user_i)) if list_item_rate_by_user_i[i] in movie_id]
                #print(index)
                list_item_bert_embedding_of_user_i = item_bert_embedding_matrix[:,
                                                                                index]
            else:
                list_item_bert_embedding_of_user_i = [[]]

            user_bert_embedding_of_user_i = np.mean(
                list_item_bert_embedding_of_user_i, axis=1)  # cal average

            if np.isnan(user_bert_embedding_of_user_i[0]):
                user_bert_embedding_matrix[:, i] = 0
            else:
                user_bert_embedding_matrix[:,
                                           i] = user_bert_embedding_of_user_i

            # user_bert_embedding_matrix[i] = user_bert_embedding_of_user_i # Gán vào ma trận user_bert_embedding trung bình item

        return user_bert_embedding_matrix

    def similarity(self):
        eps = 1e-6
        if self.bert:
            item_bert_embedding = self.bert_model.train(self.merged_text)
            if self.uuCF:
                user_bert_embedding = self.cal_user_embedding(
                    self.rating_array, item_bert_embedding)
                self.tich_hop_matran = np.concatenate(
                    (self.rating_array, user_bert_embedding), axis=0)
            else:
                self.tich_hop_matran = np.concatenate(
                    (self.rating_array, item_bert_embedding), axis=0)
            self.S = self.dist_func(
                self.tich_hop_matran.T, self.tich_hop_matran.T)
        else:
            self.S = self.dist_func(self.rating_array.T, self.rating_array.T)

    def cosine_similarity_n_space(self, m1, m2, batch_size=100):
        assert m1.shape[1] == m2.shape[1] and isinstance(
            batch_size, int) == True

        ret = np.ndarray((m1.shape[0], m2.shape[0]))

        batches = m1.shape[0] // batch_size

        if m1.shape[0] % batch_size != 0:
            batches = batches + 1

        for row_i in range(0, batches):
            start = row_i * batch_size
            end = min([(row_i + 1) * batch_size, m1.shape[0]])
            rows = m1[start: end]
            sim = cosine_similarity(rows, m2)
            ret[start: end] = sim
            # print(ret[start: end].shape)

        return ret

    def calc_sim(self, A):
        similarity = np.dot(A, A.T)
        # squared magnitude of preference vectors (number of occurrences)
        square_mag = np.diag(similarity)
        # inverse squared magnitude
        inv_square_mag = 1 / square_mag
        # if it doesn't occur, set it's inverse magnitude to zero (instead of inf)
        inv_square_mag[np.isinf(inv_square_mag)] = 0
        # inverse of the magnitude
        inv_mag = np.sqrt(inv_square_mag)
        # cosine similarity (elementwise multiply by inverse magnitudes)
        cosine = similarity * inv_mag
        return cosine.T * inv_mag

    def refresh(self):
        """
        Normalize data and calculate similarity matrix again (after
        some few ratings added)
        """
        self.normalize_Y()
        self.similarity()

    def fit(self):
        self.refresh()

    def __pred(self, u, i, normalized=1):
        """ 
        predict the rating of user u for item i (normalized)
        if you need the un
        """
        # Step 1: find all users who rated i
        ids = np.where(self.Y_data[:, 1] == i)[0].astype(np.int32)
        # Step 2:
        users_rated_i = (self.Y_data[ids, 0]).astype(np.int32)
        # Step 3: find similarity btw the current user and others
        # who already rated i
        sim = self.S[int(u), users_rated_i]
        # Step 4: find the k most similarity users
        # a = np.argsort(sim)[:self.k]
        a = np.argsort(sim)[-self.k:]
        # and the corresponding similarity levels
        nearest_s = sim[a]
        # How did each of 'near' users rated item i
        r = self.Ybar[int(i), users_rated_i[a]]
        if normalized:
            # add a small number, for instance, 1e-8, to avoid dividing by 0
            return (r*nearest_s)[0]/(np.abs(nearest_s).sum() + 1e-8)

        return (r*nearest_s)[0]/(np.abs(nearest_s).sum() + 1e-8) + self.mu[int(u)]

    def pred(self, u, i, normalized=1):
        """ 
        predict the rating of user u for item i (normalized)
        if you need the un
        """
        if self.uuCF:
            return self.__pred(u, i, normalized)
        return self.__pred(i, u, normalized)

    def recommend(self, u):
        """
        Determine all items should be recommended for user u.
        The decision is made based on all i such that:
        self.pred(u, i) > 0. Suppose we are considering items which 
        have not been rated by u yet. 
        """
        ids = np.where(self.Y_data[:, 0] == u)[0]
        items_rated_by_u = self.Y_data[ids, 1].tolist()
        recommended_items = []
        ratings = []
        for i in range(self.n_items):
            if i not in items_rated_by_u:
                rating = self.__pred(u, i, normalized = 0)
                if rating > 5:
                    rating = 5
                if rating > 0:
                    recommended_items.append(i+1)
                    ratings.append(rating)
        if self.uuCF:
            recommend_results = pd.DataFrame({'predict_rate':ratings,'movie_id': recommended_items,})
        else:
            recommend_results = pd.DataFrame({'predict_rate':ratings,'user_id': recommended_items,})
        return recommend_results

    def list_rating_label_by_u(self, u):
        ids = np.where(self.Y_data[:, 0] == int(u))[0]
        y_label = self.Y_data[ids, 2].tolist()
        return y_label

    def list_item_rate_by_u(self, u):
        ids = np.where(self.Y_data[:, 0] == int(u))[0]
        items_rated_by_u = self.Y_data[ids, 1].tolist()
        return items_rated_by_u
    #---------------------Create mask to color Pandastable result
    def matrix_to_colortable_i_i(self):
        matrix_color_i_i = []
        for u in range(self.n_items):
            ids = np.where(self.Y_data[:, 1] == int(u))[0]
            items_rated_by_u = self.Y_data[ids, 0].tolist()
            matrix_color_i_i.append(items_rated_by_u)
        return matrix_color_i_i
    
    def matrix_to_colortable_u_u(self):
        matrix_color_u_u = []
        for i in range(self.n_items):
            ids = np.where(self.Y_data[:, 1] == int(i))[0]
            users_rated_i = self.Y_data[ids, 0].tolist()
            matrix_color_u_u.append(users_rated_i)
        return matrix_color_u_u
    #---------------------Create mask to color Pandastable result

    def print_recommendation(self):
        """
        print all items which should be recommended for each user 
        """
        print('Recommendation: ')
        for u in range(self.n_users):
            recommended_items = self.recommend(u)
            if self.uuCF:
                print('    Recommend item(s):',
                      recommended_items, 'for user', u)
            else:
                print('    Recommend item', u,
                      'for user(s) : ', recommended_items)

    def full_Y(self):
        x, y = np.where(self.rating_array == 0)
        
        rating_list = self.rating_array.tolist()
        for i in range(x.shape[0]):
            # print(y[i])
            if self.uuCF:
                rating_list[x[i]][y[i]] = self.pred(y[i], x[i], 0)
            else:
                rating_list[x[i]][y[i]] = self.pred(x[i], y[i], 0)
        self.rating_array = np.array(rating_list).astype(np.float32)
        result = pd.DataFrame(self.rating_array)
        new_index = pd.RangeIndex(start=1,stop=self.rating_array.shape[1]+1,step=1)
        result.columns = new_index
        
        return result
