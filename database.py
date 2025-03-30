def read_epw(file_path, base_year=2023):
    try:
        df = pd.read_csv(file_path, skiprows=8, header=None)
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, skiprows=8, header=None, encoding='latin-1')
    
    # Select relevant columns and convert to proper types
    df = df.iloc[:, [0, 1, 2, 3, 6]]
    df.columns = ['Year', 'Month', 'Day', 'Hour', 'Temperature']
    
    # Convert numeric columns to integers
    df[['Year', 'Month', 'Day', 'Hour']] = df[['Year', 'Month', 'Day', 'Hour']].astype(int)
    
    # Convert temperature to float
    df['Temperature'] = df['Temperature'].astype(float)
    
    df['DateTime'] = df.apply(lambda row: convert_hour(row, base_year), axis=1)
    return df.set_index('DateTime')[['Temperature']]

def convert_hour(row, base_year):
    hour = row['Hour']
    if hour == 24:
        dt = datetime(base_year, row['Month'], row['Day']) + pd.DateOffset(days=1)
        return dt.replace(hour=0)
    return datetime(base_year, row['Month'], row['Day'], hour-1)
