# optimizer.py

import optuna
import pandas as pd
from typing import Tuple, Any
from .utility import split_data
from .model import RidgeRegressionModel, RandomForestModel

class Optimize():
    def __init__(self, model_class: Any, target: pd.Series, features: pd.DataFrame) -> None:
        self.model_class = model_class
        self.target = target
        self.features = features
    
    def objective(self, trial):

        params = self.get_model_params(trial)
        X_train, X_val, y_train, y_val = split_data(features=self.features, target=self.target, split=0.2)
        
        model = self.model_class(**params)
        model.fit_model(X_train, y_train)
        val_mse = model.evaluate(X_val, y_val)
        
        return val_mse

    def optimize(self, n_trials: int = 100) -> Tuple[float, optuna.study.Study]:
        study = optuna.create_study(direction='minimize')
        study.optimize(self.objective, n_trials=n_trials)
        return study.best_value, study
    
    def get_model_params(self, trial) -> dict:
        # Define hyperparameters to optimize based on the model class
        params = {}
        # Example for Ridge regression
        if self.model_class == RidgeRegressionModel:
            params['alpha'] = trial.suggest_loguniform('alpha', 1e-5, 10.0)
        # Example for RandomForest
        elif self.model_class == RandomForestModel:
            params['n_estimators'] = trial.suggest_int('n_estimators', 10, 100)
            params['max_depth'] = trial.suggest_int('max_depth', 3, 10)
            # Add more hyperparameters as needed
        
        return params
