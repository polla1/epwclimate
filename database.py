import pandas as pd
from datetime import datetime

def read_epw(file_path, base_year=2023):
    try:
        df = pd.read_csv(file_path, skiprows=8, header=None)
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, skiprows=8, header=None, encoding='latin-1')
    
    df = df.iloc[:, [0, 1, 2, 3, 6]]
    df.columns = ['Year', 'Month', 'Day', 'Hour', 'Temperature']
    df['DateTime'] = df.apply(lambda row: convert_hour(row, base_year), axis=1)
    return df.set_index('DateTime')[['Temperature']]

def convert_hour(row, base_year):
    hour = int(row['Hour'])
    if hour == 24:
        dt = datetime(base_year, row['Month'], row['Day']) + pd.DateOffset(days=1)
        return dt.replace(hour=0)
    return datetime(base_year, row['Month'], row['Day'], hour-1)

def load_baseline():
    return read_epw('2023_scenario_Erbil-Baseline.epw')

def load_2050():
    return read_epw('2050_scenario_Erbil.epw')

def load_2080():
    return read_epw('2080_scenario_Erbil.epw')
