import myfm

class Algorithm(myfm.MyFMGibbsRegressor) :
    def __init__(self):
        super().__init__(rank=10,random_seed=42,)


