import pandas as pd
from datetime import datetime
import io

def read_epw(file, base_year=2023):
    try:
        # Read the file directly from the uploaded file stream
        df = pd.read_csv(file, skiprows=8, header=None)
    except UnicodeDecodeError:
        df = pd.read_csv(file, skiprows=8, header=None, encoding='latin-1')
    
    # Convert to proper data types
    df = df.iloc[:, [0, 1, 2, 3, 6]]
    df.columns = ['Year', 'Month', 'Day', 'Hour', 'Temperature']
    df = df.apply(pd.to_numeric, errors='coerce').dropna()
    
    df['DateTime'] = df.apply(lambda row: datetime(
        base_year,
        int(row['Month']),
        int(row['Day']),
        int(row['Hour'])-1 if int(row['Hour']) != 24 else 0
    ), axis=1)
    
    return df.set_index('DateTime')[['Temperature']]

def load_baseline(file=None):
    if file:
        return read_epw(file)
    return read_epw('2023_scenario_Erbil-Baseline.epw')

def load_2050(file=None):
    if file:
        return read_epw(file)
    return read_epw('2050_scenario_Erbil.epw')

def load_2080(file=None):
    if file:
        return read_epw(file)
    return read_epw('2080_scenario_Erbil.epw')
