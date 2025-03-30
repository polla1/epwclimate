import pandas as pd
from datetime import datetime

def read_epw(file_path):
    try:
        df = pd.read_csv(file_path, skiprows=8, header=None)
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, skiprows=8, header=None, encoding='latin-1')
    
    # Select relevant columns: Month, Day, Hour, Temperature (column 6)
    df = df.iloc[:, [1, 2, 3, 6]]
    df.columns = ['Month', 'Day', 'Hour', 'Temperature']
    
    # Convert to numeric types
    df = df.apply(pd.to_numeric, errors='coerce').dropna()
    
    # Create datetime index with dummy year 2023
    df['DateTime'] = df.apply(lambda row: datetime(
        2023,  # Unified year for all data
        int(row['Month']),
        int(row['Day']),
        int(row['Hour']) - 1 if int(row['Hour']) != 24 else 0
    ), axis=1)
    
    # Add month names
    df['MonthName'] = df['DateTime'].dt.strftime('%B')
    
    return df.set_index('DateTime')[['Temperature', 'MonthName']]

def load_baseline():
    return read_epw('2023_scenario_Erbil-Baseline.epw')

def load_2050():
    return read_epw('2050_scenario_Erbil.epw')

def load_2080():
    return read_epw('2080_scenario_Erbil.epw')
