"""Prepare data for Plotly Dash."""
import numpy as np
import pandas as pd
from pathlib import Path
import os

def create_dataframe():
    """Create Pandas DataFrame from uploaded CSV."""
    uploads_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'uploads')
    # uploads_folder = Path(str(Path.cwd()) + '/uploads')

    # Check if the uploads folder exists
    if os.path.exists(uploads_folder): 
        csv_files = [f for f in os.listdir(uploads_folder) if f.endswith('.csv')]
    else:
        return pd.DataFrame(columns=["key", "created", "agency", "agency_name", "complaint_type", "descriptor", "incident_zip", "city", "latitude", "longitude"])

    if not csv_files:
        raise FileNotFoundError("No CSV files found in the 'uploads' folder")

    csv_file_path = os.path.join(uploads_folder, csv_files[0])

    df = pd.read_csv(csv_file_path, parse_dates=["created"])
    df["created"] = df["created"].dt.date
    df.drop(columns=["incident_zip"], inplace=True)
    num_complaints = df["complaint_type"].value_counts()
    to_remove = num_complaints[num_complaints <= 30].index
    df.replace(to_remove, np.nan, inplace=True)

    return df
