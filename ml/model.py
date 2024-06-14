import pandas as pd
import numpy as np
from typing import List, Tuple
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from .utility import split_data
from sklearn.preprocessing import StandardScaler

class RidgeRegressionModel():
    def __init__(self, features: pd.DataFrame, target: pd.Series, alpha=0.1) -> None:
        self.alpha = alpha
        self.model = Ridge(alpha=self.alpha)
        self.feature_columns = features.columns
        self.X_train, self.X_test, self.y_train, self.y_test = self.scale_variables(features=features, target=target)
        self.metadata = {}

    def scale_variables(self, features: pd.DataFrame, target: pd.Series) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(features)
        y = target.values  # Convert target Series to numpy array
        
        X_train, X_test, y_train, y_test = split_data(features=X_scaled, target=y)

        return X_train, X_test, y_train, y_test
        
    def fit_model(self):
        self.model.fit(self.X_train, self.y_train)
        self.metadata['num_features'] = self.X_train.shape[1]
        self.metadata['model_coefficients'] = self.model.coef_
        self.metadata['intercept'] = self.model.intercept_
        self.metadata['mse'] = self.evaluate()
        self.metadata['feature_importance'] = self._feature_importance(feature_names=self.feature_columns)
    
    def predict(self):
        prediction = self.model.predict(self.X_test)
        return prediction

    def evaluate(self):
        y_pred = self.predict()
        mse = mean_squared_error(self.y_test, y_pred)
        return mse
    
    def _feature_importance(self, feature_names: List[str]):
        if not hasattr(self.model, 'coef_'):
            raise ValueError("Model is not fitted yet. Please fit the model before getting feature importances.")
        feature_importances = pd.Series(self.model.coef_, index=feature_names)
        return feature_importances.to_dict()
        
class RandomForestModel():
    def __init__(self, n_estimators=100, max_depth=5) -> None:
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.model = RandomForestRegressor(n_estimators=self.n_estimators, max_depth=self.max_depth)
        self.metadata = {}

    def fit_model(self, X_train, y_train):
        self.model.fit(X_train, y_train)
        self.metadata['num_features'] = X_train.shape[1]
        self.metadata['feature_importance'] = self.model.feature_importances_
    
    def predict(self, X_test):
        prediction = self.model.predict(X_test)
        return prediction

    def evaluate(self, X_test, y_test):
        y_pred = self.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        self.metadata['mse'] = mse
        return mse