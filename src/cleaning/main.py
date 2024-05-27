# Main cleaning file
import pandas as pd
from .clean import fill_na_with_median_and_mode, remove_outliers, convert_datetime_column
from .read import get_data_files, concatenate_csv_files
from .reporting import define_report_structure, export_report
from .utility import count_nans_per_column, count_outliers


def run_data_cleaning(directory_path: str) -> pd.DataFrame:
    # Load data into dataframe
    file_paths = get_data_files(dir_path=directory_path)
    df = concatenate_csv_files(files=file_paths)

    # Pre-Cleaning reporting
    report = define_report_structure()
    outliers = count_outliers(df=df)
    for outlier, value in outliers.items():
        report["Category"].append("Pre-cleaned outliers")
        report["Field Description"].append(outlier)
        report["Count"].append(value)

    nan_counts = count_nans_per_column(df=df)
    for column, count in nan_counts.items():
        report["Category"].append("Pre-cleaned NaN Counts")
        report["Field Description"].append(column)
        report["Count"].append(count)

    # cleaning
    df = fill_na_with_median_and_mode(df=df)
    df = remove_outliers(df=df)
    df = convert_datetime_column(df=df)

    # Post cleaning reporting
    outliers = count_outliers(df=df)
    for outlier, value in outliers.items():
        report["Category"].append("Post-cleaned outliers")
        report["Field Description"].append(outlier)
        report["Count"].append(value)

    nan_counts = count_nans_per_column(df=df)
    for column, count in nan_counts.items():
        report["Category"].append("Post-cleaned NaN Counts")
        report["Field Description"].append(column)
        report["Count"].append(count)

    export_report(report=report)
    print(
        "Cleaning Report has been exported"
    )  # Might be useful to have a reporting screen on our data in the UI


if __name__ == "__main__":
    directory_path = "./.data"
    run_data_cleaning(directory_path=directory_path)
