import pandas as pd
from .feature_engineering import preprocess_data
from .utility import get_top_n_features
from .model import RidgeRegressionModel, XGBoostModel
from .forecasts import (data_preprocessing,
                         forecast_features_for_coin)
from src.visualizations.plot_predictions import plot_base_outcome,plot_predicted_outcome,initialize_plot

def run_regressor(df: pd.DataFrame) -> None:
    coin_names = ["Bitcoin","Cardano"]
    new_df = preprocess_data(df=df)
    X = new_df.drop(columns=['Close', 'Open'])
    y = new_df['Close']

    ridge_model = RidgeRegressionModel(features=X, target=y)
    ridge_model.fit_model()
    ridge_metadata = ridge_model.metadata
    ridge_metadata = get_top_n_features(model_metadata=ridge_metadata, n=5)
    predictions = ridge_model.predict_specific_coin(df=new_df, coin_names=coin_names)
    fig = initialize_plot()
    fig = plot_base_outcome(df=df[df['Name'].isin(values=coin_names)], x_column_name='Date', y_column_name='Close',fig=fig)
    fig = plot_predicted_outcome(df=predictions, x_column_name='Date', y_column_name='Predicted_Close', fig=fig)
    fig.show()


def run_gbm(df: pd.DataFrame) -> None:
    new_df = preprocess_data(df=df)
    X = new_df.drop(columns=['Close', 'Open'])
    y = new_df['Close']

    xgb_model = XGBoostModel(features=X, target=y)
    xgb_model.fit_model()
    coin_names = ["Bitcoin","Cardano"]
    predictions = xgb_model.predict_specific_coin(df=new_df, coin_names=coin_names)
    print(predictions)

    fig = initialize_plot()
    fig = plot_base_outcome(df=df[df['Name'].isin(values=["Bitcoin","Cardano"])], x_column_name='Date', y_column_name='Close',fig=fig)
    fig = plot_predicted_outcome(df=predictions, x_column_name='Date', y_column_name='Predicted_Close', fig=fig)
    fig.show()




# Need to one_hot_encode the data



if __name__ == "__main__":
    df = pd.read_csv("./.data/coins.csv")
    run_regressor(df=df)
    run_gbm(df=df)
