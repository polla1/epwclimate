import streamlit as st
import pandas as pd
import altair as alt
from database import load_baseline, load_2050, load_2080, read_epw
from sidebar import display_sidebar
from contact import display_contact

# Color palette for Erbil scenarios
ERBIL_COLORS = {
    '2023 Baseline': '#00FF00',  # Green
    '2050 Projection': '#0000FF',  # Blue
    '2080 Projection': '#FF0000'  # Red
}

def create_chart(data, colors, title):
    # ... (keep existing yearly chart code unchanged) ...

@st.cache_data
def load_erbil_data():
    # ... (keep existing code unchanged) ...

def main():
    # ... (keep header and yearly section code unchanged) ...

    # Fixed Monthly Analysis Section
    st.header("Monthly Temperature Analysis (Erbil)")
    month = st.selectbox(
        "Select Month", 
        range(1, 13), 
        format_func=lambda x: pd.Timestamp(2023, x, 1).strftime('%B'),
        key="month_select"
    )
    
    monthly_data = erbil_data[erbil_data.index.month == month]
    
    # Create Altair chart with day-only formatting
    monthly_chart = alt.Chart(monthly_data.reset_index()).mark_line().encode(
        x=alt.X('DateTime:T', title='Day of Month', 
               axis=alt.Axis(format='%d', labelFlush=True)),
        y=alt.Y('Temperature:Q', title='Temperature (°C)'),
        color=alt.Color('variable:N').scale(
            domain=list(ERBIL_COLORS.keys()),
            range=list(ERBIL_COLORS.values())
        ),
        tooltip=[
            alt.Tooltip('DateTime:T', title='Date', format='%b %d'),
            alt.Tooltip('Temperature:Q', format='.1f°C')
        ]
    ).properties(
        width=800,
        title=f"{pd.Timestamp(2023, month, 1).strftime('%B')} Daily Temperatures"
    )
    
    st.altair_chart(monthly_chart, use_container_width=True)

    display_contact()
