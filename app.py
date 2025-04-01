import streamlit as st
import pandas as pd
import altair as alt
from database import load_baseline, load_2050, load_2080, read_epw
from sidebar import display_sidebar
from contact import display_contact

# Define color scheme for Erbil climate scenarios
ERBIL_COLORS = {
    '2023 Baseline': '#00FF00',  # Green
    '2050 Projection': '#0000FF',  # Blue
    '2080 Projection': '#FF0000'   # Red
}

def create_chart(data, colors, title, x_axis='DateTime:T', x_format='%B'):
    """Creates a line chart with specified colors and X-axis format."""
    df_melted = data.reset_index().melt(
        id_vars=['DateTime'],
        var_name='Scenario',
        value_name='Temperature'
    )
    
    chart = alt.Chart(df_melted).mark_line(
        opacity=0.7,
        strokeWidth=2
    ).encode(
        x=alt.X(x_axis, title='Month', axis=alt.Axis(format=x_format)),  # Shows full month names
        y=alt.Y('Temperature:Q', title='Temperature (°C)'),
        color=alt.Color('Scenario:N').scale(
            domain=list(colors.keys()),
            range=list(colors.values())
        ),
        tooltip=['Scenario', 'DateTime', alt.Tooltip('Temperature:Q', format='.1f')]
    ).properties(
        height=400,
        title=title
    )
    return chart

@st.cache_data
def load_erbil_data():
    """Loads and caches climate data for Erbil."""
    data = pd.concat([
        load_baseline().rename(columns={'Temperature': '2023 Baseline'}),
        load_2050().rename(columns={'Temperature': '2050 Projection'}),
        load_2080().rename(columns={'Temperature': '2080 Projection'})
    ], axis=1)
    data.index = pd.to_datetime(data.index)  # Ensure DateTime index is properly formatted
    return data

def main():
    st.set_page_config(page_title="Climate Analysis", layout="wide")
    st.title("Climate Data Visualization")
    
    # Load Erbil climate data
    erbil_data = load_erbil_data()
    
    # Sidebar for file uploads
    uploaded_files = display_sidebar()
    custom_data = {}
    for file in uploaded_files:
        custom_data[file.name] = read_epw(file)['Temperature']
    
    # Erbil Climate Scenarios Visualization
    st.header("Erbil Climate Scenarios")
    
    # Checkboxes to select scenarios
    selected_erbil = []
    cols = st.columns(3)
    scenarios = list(ERBIL_COLORS.keys())
    for i, col in enumerate(cols):
        with col:
            if st.checkbox(scenarios[i], value=True, key=f"erbil_{i}"):
                selected_erbil.append(scenarios[i])
    
    if selected_erbil:
        st.altair_chart(
            create_chart(
                erbil_data[selected_erbil],
                {k: v for k, v in ERBIL_COLORS.items() if k in selected_erbil},
                "Erbil Temperature Projections"
            ),
            use_container_width=True
        )
    else:
        st.warning("Please select at least one Erbil scenario")
    
    # Custom Uploaded Data Visualization
    if custom_data:
        st.header("Uploaded Climate Files")
        custom_df = pd.concat(custom_data.values(), axis=1)
        custom_df.columns = custom_data.keys()
        
        st.altair_chart(
            create_chart(
                custom_df,
                {name: '#FFA500' for name in custom_data.keys()},  # Orange for uploaded files
                "Uploaded Temperature Data"
            ),
            use_container_width=True
        )
    
    # Monthly Temperature Analysis
    st.header("Monthly Temperature Analysis (Erbil)")
    month = st.selectbox(
        "Select Month", 
        range(1, 13), 
        format_func=lambda x: pd.Timestamp(2023, x, 1).strftime('%B'),
        key="month_select"
    )
    
    monthly_data = erbil_data[erbil_data.index.month == month]
    
    if not monthly_data.empty:
        st.altair_chart(
            create_chart(
                monthly_data,
                ERBIL_COLORS,
                f"Hourly Temperature Trends for {pd.Timestamp(2023, month, 1).strftime('%B')}",
                x_axis='DateTime:T',
                x_format='%d'  # Ensures only day numbers are shown
            ),
            use_container_width=True
        )
    else:
        st.warning("No data available for the selected month.")
    
    # Contact Information
    display_contact()

if __name__ == "__main__":
    main()
