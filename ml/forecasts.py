import pandas as pd
from .utility import filter_by_coin
from statsmodels.tsa.arima.model import ARIMA

def data_preprocessing(df: pd.DataFrame):
    df["Date"] = pd.to_datetime(df["Date"])
    # Ensure the DataFrame is sorted by date if not already
    df.sort_values('Date', inplace=True)
    return df

def forecast_features_for_coin(coin_df, coin_name, forecast_years: int, order=(5,1,0)):
    forecasted_data = {}
    final_df = pd.DataFrame()
    coin_df["Date"] = pd.to_datetime(coin_df["Date"])
    for feature in ['High', 'Low', 'Open', 'Close', 'Volume', 'Marketcap']:
        # Fit ARIMA model for the specific feature of the coin
        model = ARIMA(coin_df[feature], order=order)
        model_fit = model.fit()

        # Forecasting ahead
        forecast_steps = 365 * forecast_years
        forecast = model_fit.forecast(steps=forecast_steps)

        # Generating future dates for the forecast
        max_date = coin_df["Date"].max()
        forecast_dates = pd.date_range(start=max_date + pd.Timedelta(days=1), periods=forecast_steps, freq='D')

        # Creating a DataFrame for the forecasted feature data
        forecast_df = pd.DataFrame({'Date': forecast_dates, f'Forecasted_{feature}': forecast})
        if final_df.empty:
            final_df = forecast_df
        else:
            final_df = pd.merge(final_df, forecast_df, on='Date', how='outer')
        
    
    final_df["Name"] = coin_name

    return final_df

def run_forecasts(df: pd.DataFrame):
    unique_coins = df["Name"].unique()
    all_forecasted_data = {}

    for coin in unique_coins:
        coin_df = filter_by_coin(coin_name=coin, df=df)
        coin_df = data_preprocessing(coin_df)  # Ensure datetime conversion and sorting
        coin_forecasts = forecast_features_for_coin(coin_df, coin,2)
        all_forecasted_data[coin] = coin_forecasts

    final_df = pd.DataFrame()
    dataframes_test = []
    for coin, coin_df in all_forecasted_data.items():
        print(coin_df.head())
        dataframes_test.append(coin_df)
    
    final_df = pd.concat(dataframes_test, ignore_index=True, axis=0)

    final_df.to_csv("./.data/forecasts.csv")

    return final_df

if __name__ == "__main__":
    df = pd.read_csv("./.data/coins.csv")
    df = data_preprocessing(df=df)
    run_forecasts(df=df)
