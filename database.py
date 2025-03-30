import pandas as pd
from datetime import datetime

def read_epw(file_path, base_year=2023):
    """Read EPW file and extract temperature data with proper datetime index"""
    try:
        # Read EPW file (skip 8 header rows)
        df = pd.read_csv(file_path, skiprows=8, header=None, encoding='latin-1', on_bad_lines='warn')
        
        # Create proper datetime index
        df['DateTime'] = pd.to_datetime(
            df.apply(lambda row: f"{base_year}-{int(row[1]):02d}-{int(row[2]):02d} {int(row[3])-1:02d}:00:00",
                     axis=1),
            errors='coerce'
        )
        
        # Select temperature column (column index 6)
        df = df.set_index('DateTime')[[6]].rename(columns={6: 'Temperature'}).dropna()
        return df
        
    except Exception as e:
        raise ValueError(f"Error reading {file_path}: {str(e)}")

def load_scenario(file_name):
    """Load a climate scenario file with error handling"""
    try:
        return read_epw(file_name)
    except Exception as e:
        raise ValueError(f"Failed to load {file_name}: {str(e)}")

def load_baseline():
    return load_scenario('2023_scenario_Erbil-Baseline.epw')

def load_2050():
    return load_scenario('2050_scenario_Erbil.epw')

def load_2080():
    return load_scenario('2080_scenario_Erbil.epw')
