import numpy as np
from sklearn.linear_model import LinearRegression
from util.settings import get_reg_model, save_reg_model

class GazeMapper:

    def __init__(self):
        self.mapper_model = get_reg_model() or LinearRegression()

    def calibrate(self, pupile_points, label_points):
        
        # preprocess
        pupiles = np.array(pupile_points).reshape(-1, 4)
        labels = np.array(label_points).reshape(-1, 2)

        # train
        self.mapper_model.fit(pupiles, labels)

        # score
        print(self.mapper_model.score(pupiles, labels))
        print(self.mapper_model.coef_)

        # save
        save_reg_model(self.mapper_model)

    def map(self, pupile_points):
        return self.mapper_model.predict(np.array(pupile_points).reshape(-1, 4))