import pandas as pd
from .feature_engineering import preprocess_data
from .utility import get_top_n_features
from .model import RidgeRegressionModel, XGBoostModel, LoadRidgeRegressionModel
from .forecasts import (data_preprocessing,
                         forecast_features_for_coin)
from src.visualizations.plot_predictions import plot_base_outcome,plot_predicted_outcome,initialize_plot
import pickle
from typing import List
import plotly.graph_objects as go

def run_regressor(df: pd.DataFrame, alpha: float = 0.1) -> None:
    coin_names = ["Bitcoin","Cardano"]
    new_df = preprocess_data(df=df)
    X = new_df.drop(columns=['Close', 'Open'])
    y = new_df['Close']

    ridge_model = RidgeRegressionModel(features=X, target=y, alpha=alpha)
    ridge_model.fit_model()
    with open('./.models/ridge_model.pkl', 'wb') as f:
        pickle.dump(ridge_model, f)
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
    with open('./.models/xgb_model.pkl', 'wb') as f:
        pickle.dump(xgb_model, f)
    coin_names = ["Bitcoin","Cardano"]
    predictions = xgb_model.predict_specific_coin(df=new_df, coin_names=coin_names)
    print(predictions)

    fig = initialize_plot()
    fig = plot_base_outcome(df=df[df['Name'].isin(values=["Bitcoin","Cardano"])], x_column_name='Date', y_column_name='Close',fig=fig)
    fig = plot_predicted_outcome(df=predictions, x_column_name='Date', y_column_name='Predicted_Close', fig=fig)
    fig.show()

def load_regression_model(file_path: str, df: pd.DataFrame, coin_names: List[str], start_date: str, end_date: str) -> go.Figure:
    # Convert 'Date' column to datetime format and then to the desired string format
    df.drop(columns=["Unnamed: 0"], inplace=True) # TODO FIX THIS
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    
    # Convert start_date and end_date to datetime format
    start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d')
    end_date = pd.to_datetime(end_date).strftime('%Y-%m-%d')
    
    # Process and plot data
    new_df = preprocess_data(df=df)
    loaded_model = LoadRidgeRegressionModel(file_path=file_path)
    predictions = loaded_model.predict_specific_coin(df=new_df, coin_names=coin_names)
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    filtered_df = filtered_df[filtered_df["Name"].isin(values=coin_names)]
    predictions["Date"] = pd.to_datetime(predictions["Date"])
    predictions = predictions[predictions["Name"].isin(values=coin_names)]
    predictions = predictions[(predictions['Date'] >= start_date) & (predictions['Date'] <= end_date)]
    
    fig = initialize_plot()
    fig = plot_base_outcome(df=filtered_df, x_column_name='Date', y_column_name='Close', fig=fig)
    fig = plot_predicted_outcome(df=predictions, x_column_name='Date', y_column_name='Predicted_Close', fig=fig)
    fig.show()
    
    return fig




# Need to one_hot_encode the data



if __name__ == "__main__":
    df = pd.read_csv('./.data/coins.csv')
    new_df = preprocess_data(df=df)
    target = new_df["Close"]
    features = new_df.drop(columns=["Close", "Open"])

    model = RidgeRegressionModel(features=features, target=target, alpha=0.1)
    model.fit_model()
    file_path = './.models/ridge_model_test.pkl'
    try:
        with open(file_path, 'wb') as f:
            pickle.dump(model, f)
        print(f"Model saved successfully to {file_path}.")
    except Exception as e:
        print(f"An error occurred while saving the model: {e}")
