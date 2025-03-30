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
    
    chart = alt.Chart(df_melted).mark_line(
        opacity=0.7,
        strokeWidth=2
    ).encode(
        x=alt.X('DateTime:T', title='Date', axis=alt.Axis(format='%b %Y')),
        y=alt.Y('Temperature:Q', title='Temperature (°C)'),
        color=alt.Color('Scenario:N').scale(
            domain=list(colors.keys()),
            range=list(colors.values())
        ),
        tooltip=[
            'Scenario',
            alt.Tooltip('DateTime:T', title='Date', format='%B %d, %Y'),
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
    try:
        return pd.concat([
            load_baseline().rename(columns={'Temperature': '2023 Baseline'}),
            load_2050().rename(columns={'Temperature': '2050 Projection'}),
            load_2080().rename(columns={'Temperature': '2080 Projection'})
        ], axis=1)
    except Exception as e:
        st.error(f"Failed to load data: {str(e)}")
        st.stop()

def main():
    st.set_page_config(page_title="Climate Analysis", layout="wide")
    st.title("Climate Data Visualization")
    
    # Load Erbil data
    erbil_data = load_erbil_data()
    
    # Handle uploaded files
    uploaded_files = display_sidebar()
    custom_data = {}
    for file in uploaded_files:
        try:
            custom_data[file.name] = read_epw(file)['Temperature']
        except Exception as e:
            st.error(f"Error reading {file.name}: {str(e)}")

    # Erbil Yearly Comparison
    st.header("Weather file (.EPW) Scenarios of Erbil")
    
    # Scenario selection
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
                "Interactive Yearly Temperature of 2023, 2050, and 2080 - Erbil, Iraq"
            ),
            use_container_width=True
        )
    else:
        st.warning("Please select at least one Erbil scenario")

    # Custom Uploads Visualization
    if custom_data:
        st.header("Uploaded Climate Files")
        custom_df = pd.concat(custom_data.values(), axis=1)
        custom_df.columns = custom_data.keys()
        
        st.altair_chart(
            create_chart(
                custom_df,
                {name: '#FFA500' for name in custom_data.keys()},
                "Uploaded Temperature Data"
            ),
            use_container_width=True
        )

    # Monthly Analysis
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
                f"{pd.Timestamp(2023, month, 1).strftime('%B')} Daily Temperatures"
            ),
            use_container_width=True
        )
    else:
        st.warning("No data available for selected month")

    display_contact()

if __name__ == "__main__":
    main()
