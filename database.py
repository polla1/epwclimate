import pandas as pd

def read_epw(file_path, base_year=2023):
    """Simplified EPW reader without external dependencies"""
    try:
        df = pd.read_csv(
            file_path, 
            skiprows=8, 
            header=None,
            encoding='latin-1',
            on_bad_lines='skip'
        )
        
        # Create datetime index
        df['DateTime'] = pd.to_datetime(
            df[[1, 2, 3]].rename(columns={
                1: 'month',
                2: 'day',
                3: 'hour'
            }).assign(year=base_year),
            format='%Y-%m-%d %H:%M:%S'
        )
        
        return df.set_index('DateTime')[[6]].rename(columns={6: 'Temperature'})
        
    except Exception as e:
        raise ValueError(f"EPW read error: {str(e)}")

# Keep the rest of your database.py the same
def load_baseline(): ...
def load_2050(): ...
def load_2080(): ...
