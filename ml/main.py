import pandas as pd
from .feature_engineering import preprocess_data
from .utility import get_top_n_features
from .model import RidgeRegressionModel
from .forecasts import (data_preprocessing,
                         forecast_features_for_coin)
from src.visualizations.plot_predictions import plot_base_outcome,plot_predicted_outcome,initialize_plot


def run(df: pd.DataFrame) -> None:
    fig = initialize_plot()
    fig = plot_base_outcome(df=df[df['Name'].isin(values=["Cardano"])], x_column_name='Date', y_column_name='Close', fig=fig)
    new_df = preprocess_data(df=df)
    print(len(new_df.columns))
    df_columns = new_df.columns
    X = new_df.drop(columns=['Close', 'Open'])
    y = new_df['Close']

    ridge_model = RidgeRegressionModel(features=X, target=y)
    ridge_model.fit_model()
    ridge_metadata = ridge_model.metadata
    ridge_metadata = get_top_n_features(model_metadata=ridge_metadata, n=5)
    # print(ridge_metadata)
    coin_names = ["Cardano"]
    predictions = ridge_model.predict_specific_coin(df=new_df, coin_names=coin_names)
    print(predictions)

    fig = plot_predicted_outcome(df=predictions, x_column_name='Date', y_column_name='Predicted_Close', fig=fig)
    fig.show()




# Need to one_hot_encode the data



if __name__ == "__main__":
    df = pd.read_csv("./.data/coins.csv")
    run(df=df)
