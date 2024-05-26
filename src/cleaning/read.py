import os
import pandas as pd
from typing import List
from .validation import validate_directory
from .load import push_to_sqlite, write_to_csv


def get_data_files(dir_path: str) -> List[str]:
    try:
        validate_directory(dir_path=dir_path)
        files = []
        for file_name in os.listdir(dir_path):
            # Check if the file is a CSV
            if file_name.endswith(".csv"):
                file_path = os.path.join(dir_path, file_name)
                files.append(file_path)

        return files
    except Exception as e:
        main_error = "IngestionError"
        sub_error = type(e).__name__  # Get the name of the error
        message = str(e)
        print(f"Main Error: {main_error}\nSub Error: {sub_error}\nMessage: {message}")
        return []


def concatenate_csv_files(files: List[str]) -> pd.DataFrame:
    data_frames = []
    sum_lengths = 0
    for file_path in files:
        df = pd.read_csv(file_path)
        sum_lengths += len(df)
        data_frames.append(df)

    concatenated_df = pd.concat(data_frames, ignore_index=True)
    return concatenated_df


if __name__ == "__main__":
    file_path = get_data_files(".data")
    df = concatenate_csv_files(files=file_path)
    write_to_csv(df=df)
    # push_to_sqlite(df=df, table_name="CoinsTable")
