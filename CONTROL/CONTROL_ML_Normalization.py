import numpy as np
from CONTROL_normalization import CONTROL_normalization
from sklearn.model_selection import train_test_split


class CONTROL_ML_Normalization:
    def __init__(self):
        self.notification = None
        self.normalize_engine = CONTROL_normalization()
        pass

    def Test(self, df):
        try:
            
            # Example về thay đổi df --> chỗ này thay đổi thanh hàm
            # df['randNumCol'] = np.random.randint(1, 6, df.shape[0])
            # set up trước khi chuẩn hóa
            full_feature_dataset = df.copy()
            df_train, df_test = train_test_split(
                full_feature_dataset, test_size=0.2)
            df_train_tosave = df_train.copy()
            df_test_tosave = df_test.copy()
            # tìm những feature tốt nhất cho tập dữ liệu
            full_feature_rmse = self.normalize_engine.full_feature_rmse(
                full_feature_dataset, df_train, df_test)
            self.normalize_engine.best_features(
                full_feature_dataset, df_train, df_test, full_feature_rmse)
            
            # tạo ra dataset mới từ những feature tốt nhất
            newData = self.normalize_engine.new_dataset(
                df_train_tosave, df_test_tosave)
            self.notification = "Process is done!"
            return newData
        except:
            self.notification = "Process is fail, try again!"

    def alert(self):
        return self.notification
