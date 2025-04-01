import pandas as pd
import io

def read_epw(file):
    try:
        # Read the file content and decode it
        content = file.read().decode("utf-8")  # Decode for safe processing
        file.seek(0)  # Reset file pointer after reading

        # Read EPW data, skipping metadata (first 8 rows)
        df = pd.read_csv(io.StringIO(content), skiprows=8, header=None)

        # Ensure the required Temperature column exists (column index might vary)
        if df.empty or df.shape[1] < 7:  # Change index if necessary
            raise ValueError("EPW file format issue: Missing necessary columns.")

        df.columns = ["Year", "Month", "Day", "Hour", "Minute", "DataSource", "Temperature"]  # Adjust column names

        df["DateTime"] = pd.to_datetime(df[["Year", "Month", "Day", "Hour"]])
        df.set_index("DateTime", inplace=True)

        return df[["Temperature"]]  # Return only necessary columns

    except Exception as e:
        raise ValueError(f"Error reading EPW file: {e}")
