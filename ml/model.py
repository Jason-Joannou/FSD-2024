import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

class regressionModel():
    def __init__(self, alpha=1.0) -> None:
        self.alpha = alpha
        self.model = Ridge(alpha=self.alpha)

    def fit_model(self, X_train, y_train):
        self.model.fit(X_train, y_train)
    
    def predict(self, X_test):
        prediction = self.model.predict(X_test)
        return prediction

    def evaluate(self, X_test, y_test):
        y_pred = self.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        return mse
