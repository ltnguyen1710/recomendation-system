import numpy as np

class CONTROL_ML_Normalization:
    def __init__(self):
        self.notification = None
        pass
        
    def Test(self,df):
        try:
            # Example về thay đổi df --> chỗ này thay đổi thanh hàm
            df['randNumCol'] = np.random.randint(1, 6, df.shape[0])
            self.notification = "Process is done!"
        except:
            self.notification = "Process is fail, try again!"

    def  alert(self):
        return self.notification

        



    
