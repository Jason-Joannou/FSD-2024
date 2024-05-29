import optuna
import pandas as pd
from typing import Tuple, Any
from .utility import split_data

class Optimize():
    def __init__(self, params: Tuple, target: pd.Series, features: pd.DataFrame, model: Any) -> None:
        self.target = target
        self.features = features
    
    def objective(trial):
        pass

