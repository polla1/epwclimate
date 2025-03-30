import streamlit as st
import pandas as pd
import altair as alt
from database import load_baseline, load_2050, load_2080, read_epw
from sidebar import display_sidebar
from contact import display_contact

ERBIL_COLORS = {
    '2023 Baseline': '#00FF00',
    '2050 Projection': '#0000FF',
    '2080 Projection': '#FF0000'
}

def create_chart(data, colors, title):
    """Create a line chart with month-only x-axis"""
    # Add MonthName column from index
    df = data.copy()
    df['Month'] = df.index.strftime('%B')
    
    # Melt data for Altair
    df_melted = df.melt(
        id_vars=['Month'],
        var_name='Scenario',
        value_name='Temperature'
    )
    
    # Define month order
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # Build chart
    chart = alt.Chart(df_melted).mark_line(
        opacity=0.7,
        strokeWidth=2
    ).encode(
        x=alt.X('Month:N', title='Month',
               sort=month_order,
               axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Temperature:Q', title='Temperature (°C)'),
        color=alt.Color('Scenario:N').scale(
            domain=list(colors.keys()),
            range=list(colors.values())
        ),
        tooltip=[
            'Month',
            'Scenario',
            alt.Tooltip('Temperature:Q', format='.1f°C')
        ]
    ).properties(
        height=400,
        title=title
    )
    return chart

@st.cache_data
def load_erbil_data():
    """Load and cache Erbil climate data"""
    baseline = load_baseline().rename(columns={'Temperature': '2023 Baseline'})
    proj2050 = load_2050().rename(columns={'Temperature': '2050 Projection'})
    proj2080 = load_2080().rename(columns={'Temperature': '2080 Projection'})
    return pd.concat([baseline, proj2050, proj2080], axis=1)

def main():
    st.set_page_config(page_title="Climate Analysis", layout="wide")
    st.title("Climate Data Visualization")
    
    # Load data
    erbil_data = load_erbil_data()
    
    # Handle uploaded files
    uploaded_files = display_sidebar()
    custom_data = {}
    for file in uploaded_files:
        df = read_epw(file)
        custom_data[file.name] = df['Temperature']

    # Scenario selection
    st.header("Weather file (.EPW) Scenarios of Erbil")
    selected = []
    cols = st.columns(3)
    for i, scenario in enumerate(ERBIL_COLORS):
        with cols[i]:
            if st.checkbox(scenario, True, key=f"scen_{i}"):
                selected.append(scenario)

    if selected:
        st.altair_chart(
            create_chart(erbil_data[selected],
                        {k: ERBIL_COLORS[k] for k in selected},
                        "Monthly Temperature Comparison"),
            use_container_width=True
        )
    else:
        st.warning("Please select at least one scenario")

    # Custom uploads
    if custom_data:
        st.header("Uploaded Climate Files")
        custom_df = pd.concat(custom_data.values(), axis=1)
        custom_df.columns = custom_data.keys()
        
        st.altair_chart(
            create_chart(custom_df,
                        {name: '#FFA500' for name in custom_data.keys()},
                        "Uploaded Temperature Data"),
            use_container
