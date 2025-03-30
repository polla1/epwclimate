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
    """Create a line chart with specified colors"""
    df_melted = data.reset_index().melt(
        id_vars=['DateTime'],
        var_name='Scenario',
        value_name='Temperature'
    )
    
    # Custom axis formatting based on chart type
    if "Yearly" in title:
        x_axis = alt.X('DateTime:T', title='Month', 
                      axis=alt.Axis(format='%b', labelAngle=0))
    else:
        x_axis = alt.X('DateTime:T', title='Date')
    
    chart = alt.Chart(df_melted).mark_line(
        opacity=0.7,
        strokeWidth=2
    ).encode(
        x=x_axis,
        y=alt.Y('Temperature:Q', title='Temperature (°C)'),
        color=alt.Color('Scenario:N').scale(
            domain=list(colors.keys()),
            range=list(colors.values())
        ),
        tooltip=['Scenario', alt.Tooltip('Temperature:Q', format='.1f')]
    ).properties(
        height=400,
        title=title
    )
    return chart

@st.cache_data
def load_erbil_data():
    """Load and cache Erbil climate data"""
    return pd.concat([
        load_baseline().rename(columns={'Temperature': '2023 Baseline'}),
        load_2050().rename(columns={'Temperature': '2050 Projection'}),
        load_2080().rename(columns={'Temperature': '2080 Projection'})
    ], axis=1)

def main():
    st.set_page_config(page_title="Climate Analysis", layout="wide")
    st.title("Climate Data Visualization")
    
    # Load Erbil data
    erbil_data = load_erbil_data()
    
    # Handle uploaded files
    uploaded_files = display_sidebar()
    custom_data = {}
    for file in uploaded_files:
        custom_data[file.name] = read_epw(file)['Temperature']

    # Rest of the code remains the same as previous version...
    # [Include all other sections unchanged]

if __name__ == "__main__":
    main()
