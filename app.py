import streamlit as st
import pandas as pd
from database import load_baseline, load_2050, load_2080, read_epw
from sidebar import display_sidebar
from contact import display_contact

def main():
    st.title("Erbil City Temperature Analysis")
    
    # Load baseline data
    baseline = load_baseline()
    future_2050 = load_2050()
    future_2080 = load_2080()
    
    # Combine data
    combined = pd.concat([
        baseline.rename(columns={'Temperature': 'Baseline 2023'}),
        future_2050.rename(columns={'Temperature': 'Future 2050'}),
        future_2080.rename(columns={'Temperature': 'Future 2080'})
    ], axis=1)

    # Process uploaded files
    uploaded_files = display_sidebar()
    for file in uploaded_files:
        temp_df = read_epw(file)
        combined[file.name] = temp_df['Temperature']

    # Yearly visualization
    st.header("Yearly Temperature Comparison")
    st.line_chart(combined)

    # Monthly analysis
    st.header("Monthly Analysis")
    month = st.selectbox("Select Month", range(1,13), 
                        format_func=lambda x: pd.Timestamp(2023, x, 1).strftime('%B'))
    
    monthly_data = combined[combined.index.month == month]
    st.line_chart(monthly_data)

    display_contact()

if __name__ == "__main__":
    main()
