import kaggle
import argparse
from .validation import validate_dataset_name

def load_kaggle_data(dataset_name: str, unzip: bool = True, path: str = "./.data") -> None:
    """
    Downloads a Kaggle dataset and optionally unzips it.

    Args:
        dataset_name (str): The name of the Kaggle dataset to download.
        unzip (bool, optional): Whether to unzip the downloaded files. Defaults to True.
        path (str, optional): The path to download the dataset to. Defaults to "./.data".

    Raises:
        Exception: Prints the main error, sub error, and error message if an exception occurs during dataset download.
    """
    try:
        validate_dataset_name(dataset_name=dataset_name)
        kaggle.api.dataset_download_files(dataset=dataset_name, path=path, unzip=unzip)
    except Exception as e:
        main_error = "IngestionError"
        sub_error = type(e).__name__  # Get the name of the error
        message = str(e)
        print(f"Main Error: {main_error}\nSub Error: {sub_error}\nMessage: {message}")

def main():
    """
    Parses command line arguments and downloads the specified Kaggle dataset.

    Command Line Arguments:
        dataset_name (str): The name of the dataset to download.
        --unzip: Unzips the dataset files after download.
        --no-unzip: Does not unzip the dataset files after download.
        --path (str): The path to download the dataset to. Default is "./.data".

    Usage:
        python -m src.ingestion.ingestion --help
        python -m src.ingestion.ingestion sudalairajkumar/cryptocurrencypricehistory
        python -m src.ingestion.ingestion sudalairajkumar/cryptocurrencypricehistory --unzip
        python -m src.ingestion.ingestion sudalairajkumar/cryptocurrencypricehistory --no-unzip
        python -m src.ingestion.ingestion sudalairajkumar/cryptocurrencypricehistory --no-unzip --path ./
    """
    parser = argparse.ArgumentParser(description='Download a Kaggle dataset.')
    parser.add_argument('dataset_name', type=str, help='The name of the dataset to download.')
    parser.add_argument('--unzip', dest='unzip', action='store_true', help='Unzip the dataset files after download.')
    parser.add_argument('--no-unzip', dest='unzip', action='store_false', help='Do not unzip the dataset files after download.')
    parser.set_defaults(unzip=True)
    parser.add_argument('--path', type=str, default='./.data', help='The path to download the dataset to. Default is set to "./.data"')
    
    args = parser.parse_args()
    
    load_kaggle_data(dataset_name=args.dataset_name, unzip=args.unzip, path=args.path)

if __name__ == "__main__":
    main()

    # Usage
    # python -m src.ingestion.ingestion --help
    # python -m src.ingestion.ingestion sudalairajkumar/cryptocurrencypricehistory
    # python -m src.ingestion.ingestion sudalairajkumar/cryptocurrencypricehistory --unzip
    # python -m src.ingestion.ingestion sudalairajkumar/cryptocurrencypricehistory --no-unzip
    # python -m src.ingestion.ingestion sudalairajkumar/cryptocurrencypricehistory --no-unzip --path ./
