# app.py
import streamlit as st
import pandas as pd
import altair as alt
from database import load_baseline, load_2050, load_2080, read_epw
from sidebar import display_sidebar
from contact import display_contact

# 1. Color Settings - Easy to modify colors here
SCENARIO_COLORS = {
    '2023 Baseline': '#00FF00',  # Green
    '2050 Projection': '#0000FF',  # Blue
    '2080 Projection': '#FF0000'  # Red
}
UPLOAD_COLOR = '#FFA500'  # Orange for uploaded files

# 2. Chart Creation Function - Reusable for all charts
def create_chart(data, colors, title):
    """Create a temperature chart with consistent styling"""
    melted_data = data.reset_index().melt(
        id_vars=['DateTime'],
        var_name='Scenario',
        value_name='Temperature'
    )
    
    chart = alt.Chart(melted_data).mark_line(
        opacity=0.7,
        strokeWidth=2
    ).encode(
        x=alt.X('DateTime:T', title='Date'),
        y=alt.Y('Temperature:Q', title='Temperature (°C)'),
        color=alt.Color('Scenario:N').scale(
            domain=list(colors.keys()),
            range=list(colors.values())
        ),
        tooltip=[
            alt.Tooltip('DateTime:T', title='Date', format='%b %d'),
            'Scenario',
            alt.Tooltip('Temperature:Q', format='.1f°C')
        ]
    ).properties(
        height=400,
        title=title
    )
    return chart

# 3. Data Loading with Error Protection
@st.cache_data
def load_erbil_data():
    """Safely load climate data with error handling"""
    try:
        return pd.concat([
            load_baseline().rename(columns={'Temperature': '2023 Baseline'}),
            load_2050().rename(columns={'Temperature': '2050 Projection'}),
            load_2080().rename(columns={'Temperature': '2080 Projection'})
        ], axis=1)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

# 4. Main Application
def main():
    # Basic page setup
    st.set_page_config(page_title="Climate Analysis", layout="wide")
    st.title("Erbil Climate Visualization")
    
    # Load main data
    erbil_data = load_erbil_data()
    
    # File upload handling
    uploaded_files = display_sidebar()
    custom_data = {}
    
    # Process uploaded files with error handling
    for file in uploaded_files:
        try:
            custom_data[file.name] = read_epw(file)['Temperature']
        except Exception as e:
            st.error(f"Couldn't read {file.name}: {str(e)}")

    # 5. Main Scenarios Section
    st.header("Compare Climate Scenarios")
    
    # Scenario selection using checkboxes
    selected_scenarios = []
    cols = st.columns(3)  # Create 3 columns for checkboxes
    
    for i, scenario in enumerate(SCENARIO_COLORS.keys()):
        with cols[i]:  # Place each checkbox in its own column
            if st.checkbox(scenario, value=True, key=f"scenario_{i}"):
                selected_scenarios.append(scenario)

    # Show selected scenarios chart
    if selected_scenarios:
        st.altair_chart(
            create_chart(
                erbil_data[selected_scenarios],
                {k: v for k, v in SCENARIO_COLORS.items() if k in selected_scenarios},
                "Temperature Comparison Over Time"
            ),
            use_container_width=True
        )
    else:
        st.warning("Please select at least one scenario to display")

    # 6. Uploaded Files Section
    if custom_data:
        st.header("Your Uploaded Data")
        custom_df = pd.concat(custom_data.values(), axis=1)
        custom_df.columns = custom_data.keys()
        
        st.altair_chart(
            create_chart(
                custom_df,
                {name: UPLOAD_COLOR for name in custom_data.keys()},
                "Uploaded Temperature Files Comparison"
            ),
            use_container_width=True
        )

    # 7. Monthly Analysis (Improved Formatting)
    st.header("Monthly Temperature Details")
    month = st.selectbox(
        "Choose a Month:", 
        range(1, 13), 
        format_func=lambda x: pd.Timestamp(2023, x, 1).strftime('%B'),
        help="Select a month to see daily temperature patterns"
    )
    
    # Filter and format monthly data
    monthly_data = erbil_data[erbil_data.index.month == month]
    
    if not monthly_data.empty:
        # Create special chart with weekday formatting
        melted = monthly_data.reset_index().melt(id_vars=['DateTime'])
        chart = alt.Chart(melted).mark_line().encode(
            x=alt.X('DateTime:T', title='Date',
                   axis=alt.Axis(format='%a %d')),  # Format as "Tue 03"
            y=alt.Y('Temperature:Q', title='Temperature (°C)'),
            color=alt.Color('variable:N').scale(
                domain=list(SCENARIO_COLORS.keys()),
                range=list(SCENARIO_COLORS.values())
            ),
            tooltip=[
                alt.Tooltip('DateTime:T', title='Date', format='%b %d'),
                alt.Tooltip('Temperature:Q', format='.1f°C'),
                'variable:N'
            ]
        ).properties(
            title=f"{pd.Timestamp(2023, month, 1).strftime('%B')} Daily Temperatures"
        )
        
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("No data available for selected month")

    # Show contact information
    display_contact()

# 8. Start the application
if __name__ == "__main__":
    main()
