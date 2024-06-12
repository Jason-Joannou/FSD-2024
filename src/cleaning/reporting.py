import pandas as pd
from typing import Dict


def define_report_structure():
    report = {"Category": [], "Field Description": [], "Count": []}
    return report


def export_report(report: Dict) -> None:
    df = pd.DataFrame(report)
    df.to_csv("./.data/Data Report.csv")
