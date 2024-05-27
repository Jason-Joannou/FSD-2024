import kaggle
from .validation import validate_dataset_name

def load_kaggle_data(dataset_name: str, unzip: bool = True, path: str ="./.data") -> str:
    try:
        validate_dataset_name(dataset_name=dataset_name)
        kaggle.api.dataset_download_files(dataset=dataset_name, path=path, unzip=unzip)
    except Exception as e:
        main_error = "IngestionError"
        sub_error = type(e).__name__  # Get the name of the error
        message = str(e)
        print(f"Main Error: {main_error}\nSub Error: {sub_error}\nMessage: {message}")


if __name__ == "__main__":
    load_kaggle_data(dataset_name="sudalairajkumar/cryptocurrencypricehistory")