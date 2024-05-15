import pandas as pd
import os

# Function to read and clean a CSV file
def clean_coin_data(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Remove duplicate rows
    df.drop_duplicates(inplace=True)
    
    # Handle missing values
    # You can customize this part depending on your specific needs. For instance:
    # Fill missing values with 0
    df.fillna(0, inplace=True)
    
    # Convert the 'Date' column to datetime format
    df

clean_coin_data('coin_Stellar.csv')