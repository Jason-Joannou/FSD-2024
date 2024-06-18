import pandas as pd
from .feature_engineering import preprocess_data
from .utility import get_top_n_features
from .model import RidgeRegressionModel


def run(df: pd.DataFrame) -> None:
    df = preprocess_data(df=df)
    df_columns = df.columns
    X = df.drop(columns=['Close'])
    y = df['Close']

    ridge_model = RidgeRegressionModel(features=X, target=y)
    ridge_model.fit_model()
    ridge_metadata = ridge_model.metadata
    ridge_metadata = get_top_n_features(model_metadata=ridge_metadata, n=5)
    print(ridge_metadata)


# Need to one_hot_encode the data



if __name__ == "__main__":
    df = pd.read_csv("./.data/coins.csv")
    run(df=df)
