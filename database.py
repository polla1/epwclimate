import pandas as pd
from datetime import datetime
import pandas as pd

def read_epw(file_path, base_year=2023):
    try:
        df = pd.read_csv(file_path, skiprows=8, header=None)
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, skiprows=8, header=None, encoding='latin-1')
    
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

def load_baseline():
    return read_epw('2023_scenario_Erbil-Baseline.epw', base_year=2023)

def load_2050():
    return read_epw('2050_scenario_Erbil.epw', base_year=2050)  # Set to 2050

def load_2080():
    return read_epw('2080_scenario_Erbil.epw', base_year=2080)  # Set to 2080
