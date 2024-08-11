import pandas as pd
from .utility import filter_by_coin
from statsmodels.tsa.arima.model import ARIMA

def data_preprocessing(df: pd.DataFrame) -> pd.DataFrame:
    df["Date"] = pd.to_datetime(df["Date"])
    # Ensure the DataFrame is sorted by date if not already
    df.sort_values('Date', inplace=True)
    # Set the 'Date' column as the index
    df.set_index('Date', inplace=True)
    # Set the frequency of the Date index
    df = df.asfreq('D')  # Assuming daily frequency. Adjust if needed.
    return df

def forecast_features_for_coin(coin_df: pd.DataFrame, coin_name: str, forecast_years: int, order=(2, 1, 2)) -> pd.DataFrame:
    forecasted_data = {}
    final_df = pd.DataFrame()
    
    for feature in ['High', 'Low', 'Open', 'Close', 'Volume', 'Marketcap']:
        # Fit ARIMA model for the specific feature of the coin
        model = ARIMA(coin_df[feature], order=order)
        model_fit = model.fit()

        # Forecasting ahead
        forecast_steps = 365 * forecast_years
        forecast = model_fit.forecast(steps=forecast_steps)

        # Generating future dates for the forecast
        forecast_dates = pd.date_range(start=coin_df.index.max() + pd.Timedelta(days=1), periods=forecast_steps, freq='D')

        # Creating a DataFrame for the forecasted feature data
        forecast_df = pd.DataFrame({'Date': forecast_dates, f'Forecasted_{feature}': forecast})
        forecast_df.set_index('Date', inplace=True)  # Set the forecast dates as index
        
        if final_df.empty:
            final_df = forecast_df
        else:
            final_df = pd.merge(final_df, forecast_df, left_index=True, right_index=True, how='outer')
    
    final_df["Name"] = coin_name
    final_df.reset_index(inplace=True)  # Reset index to move 'Date' back to a column
    
    return final_df

def run_forecasts(df: pd.DataFrame) -> pd.DataFrame:
    unique_coins = df["Name"].unique()
    all_forecasted_data = {}

    for coin in unique_coins:
        coin_df = filter_by_coin(coin_name=coin, df=df)
        coin_df = data_preprocessing(coin_df)  # Ensure datetime conversion and sorting
        coin_forecasts = forecast_features_for_coin(coin_df, coin, 2)
        all_forecasted_data[coin] = coin_forecasts

    final_df = pd.DataFrame()
    dataframes_test = []
    for coin, coin_df in all_forecasted_data.items():
        dataframes_test.append(coin_df)
    
    final_df = pd.concat(dataframes_test, ignore_index=True, axis=0)

    # Rename only the columns that contain 'Forecasted_' and '_'
    final_df.columns = final_df.columns.str.replace('Forecasted_', '', regex=False).str.replace('_', '', regex=False)

    if "Unnamed: 0" in final_df.columns:
        final_df.drop(labels=["Unnamed: 0"], inplace=True, axis=1)

    final_df.to_csv("./.data/forecasts.csv", index=False)

    return final_df

if __name__ == "__main__":
    df = pd.read_csv("./.data/coins.csv")
    # df = data_preprocessing(df=df)
    run_forecasts(df=df)
