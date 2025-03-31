import streamlit as st
import pandas as pd
import altair as alt
from database import load_baseline, load_2050, load_2080, read_epw
from sidebar import display_sidebar
from contact import display_contact

def main():
    st.title("Erbil City Temperature Analysis")
    
    # Load data with correct base years
    baseline = load_baseline().assign(Scenario='Baseline 2023')
    future_2050 = load_2050().assign(Scenario='Future 2050')
    future_2080 = load_2080().assign(Scenario='Future 2080')
    
    # Combine data
    combined = pd.concat([baseline, future_2050, future_2080])
    
    # Process uploaded files and add to combined
    uploaded_files = display_sidebar()
    for file in uploaded_files:
        temp_df = read_epw(file).assign(Scenario=file.name)
        combined = pd.concat([combined, temp_df])
    
    # Create a common day-of-year index for comparison
    combined['DayOfYear'] = combined.index.dayofyear
    combined['Hour'] = combined.index.hour
    
    # Yearly visualization using Altair
    st.header("Yearly Temperature Comparison")
    chart = alt.Chart(combined.reset_index()).mark_line().encode(
        x=alt.X('DayOfYear:Q', title='Day of Year'),
        y='Temperature:Q',
        color='Scenario:N',
        tooltip=['DateTime:T', 'Scenario:N', 'Temperature:Q']
    ).interactive()
    st.altair_chart(chart, use_container_width=True)
    
    # Monthly analysis
    st.header("Monthly Analysis")
    month = st.selectbox("Select Month", range(1,13), format_func=lambda x: pd.Timestamp(2023, x, 1).strftime('%B'))
    
    monthly_data = combined[combined.index.month == month]
    monthly_chart = alt.Chart(monthly_data.reset_index()).mark_line().encode(
        x='DateTime:T',
        y='Temperature:Q',
        color='Scenario:N'
    )
    st.altair_chart(monthly_chart, use_container_width=True)
    
    display_contact()

if __name__ == "__main__":
    main()
