# from CF import CF
import pandas as pd
from myfm.utils.benchmark_data import MovieLens100kDataManager

data = MovieLens100kDataManager()

path = 'E:\\recommendation-system\\CONTROL\\100K - Copy (2).csv'
# train = data.load_rating_all()
movie_data = pd.read_csv(path)

print(movie_data)

# ratings_train = pd.merge(train, movie_data, on="movie_id", how='outer')
# index_to_delete = ratings_train[ratings_train['user_id'].isna()].index
# ratings_train.drop(index_to_delete, inplace=True)

# ratings_train.to_csv('100K.csv', sep=',', encoding='utf-8',index=False)

# ratings_test = pd.merge(test, movie_data, on='movie_id', how='outer')
# index_to_delete = ratings_test[ratings_test['user_id'].isna()].index
# ratings_test.drop(index_to_delete, inplace=True)

# rs = CF(ratings_train, k=20, uuCF=1, bert=1)
# rs.fit()

