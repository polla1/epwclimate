import streamlit as st
import pandas as pd
import altair as alt
from database import load_baseline, load_2050, load_2080, read_epw
from sidebar import display_sidebar
from contact import display_contact

# Color settings for Erbil scenarios
ERBIL_COLORS = {
    '2023 Baseline': '#00FF00',  # Green
    '2050 Projection': '#0000FF',  # Blue
    '2080 Projection': '#FF0000'  # Red
}

def create_chart(data, colors, title):
    """Create Altair chart with proper formatting"""
    df_melted = data.reset_index().melt(
        id_vars=['DateTime'],
        var_name='Scenario',
        value_name='Temperature'
    )
    
    # X-axis formatting
    if "Yearly" in title:
        x_axis = alt.X('DateTime:T', title='Month', 
                      axis=alt.Axis(format='%b', labelAngle=0))
    else:
        x_axis = alt.X('DateTime:T', title='Day of Month',
                      axis=alt.Axis(format='%-d', labelFlush=True))
    
    return alt.Chart(df_melted).mark_line(
        opacity=0.7,
        strokeWidth=2
    ).encode(
        x=x_axis,
        y=alt.Y('Temperature:Q', title='Temperature (°C)'),
        color=alt.Color('Scenario:N').scale(
            domain=list(colors.keys()),
            range=list(colors.values())
        ),
        tooltip=[
            alt.Tooltip('DateTime:T', title='Date', format='%b %-d'),
            alt.Tooltip('Temperature:Q', format='.1f°C'),
            'Scenario'
        ]
    ).properties(
        height=400,
        title=title
    )

@st.cache_data
def load_erbil_data():
    """Load and process Erbil EPW data"""
    return pd.concat([
        load_baseline().rename(columns={'Temperature': '2023 Baseline'}),
        load_2050().rename(columns={'Temperature': '2050 Projection'}),
        load_2080().rename(columns={'Temperature': '2080 Projection'})
    ], axis=1)

def main():
    st.set_page_config(page_title="Erbil Climate Analysis", layout="wide")
    st.title("EPW Climate Data Visualization - Erbil, Iraq")
    
    # Load core data
    erbil_data = load_erbil_data()
    
    # Handle file uploads
    uploaded_files = display_sidebar()
    custom_data = {}
    for file in uploaded_files:
        temp_df = read_epw(file)
        custom_data[file.name] = temp_df['Temperature']

    # =====================
    # Yearly Analysis Section
    # =====================
    st.header("EPW Scenarios Comparison")
    selected_scenarios = []
    cols = st.columns(3)
    for i, scenario in enumerate(ERBIL_COLORS.keys()):
        with cols[i]:
            if st.checkbox(scenario, value=True, key=f"scenario_{i}"):
                selected_scenarios.append(scenario)
    
    if selected_scenarios:
        yearly_chart = create_chart(
            erbil_data[selected_scenarios],
            {k: ERBIL_COLORS[k] for k in selected_scenarios},
            "Yearly Temperature Comparison: 2023 vs 2050 vs 2080"
        )
        st.altair_chart(yearly_chart, use_container_width=True)
    else:
        st.warning("Please select at least one scenario")

    # =====================
    # Monthly Analysis Section
    # =====================
    st.header("Monthly Temperature Profile")
    month = st.selectbox(
        "Select Month", 
        range(1, 13), 
        format_func=lambda x: pd.Timestamp(2023, x, 1).strftime('%B'),
        key="month_select"
    )
    
    # Process monthly data
    if not erbil_data.empty:
        # Filter and resample to daily averages
        monthly_data = erbil_data[erbil_data.index.month == month]
        daily_data = monthly_data.resample('D').mean()
        
        # Create and display chart
        monthly_chart = create_chart(
            daily_data,
            ERBIL_COLORS,
            f"Daily Temperature Profile - {pd.Timestamp(2023, month, 1).strftime('%B')}"
        )
        st.altair_chart(monthly_chart, use_container_width=True)
    else:
        st.warning("No data available for selected month")

    # =====================
    # Custom Uploads Section
    # =====================
    if custom_data:
        st.header("Uploaded EPW Analysis")
        custom_df = pd.concat(custom_data.values(), axis=1)
        custom_df.columns = custom_data.keys()
        
        upload_chart = create_chart(
            custom_df,
            {name: '#FFA500' for name in custom_data.keys()},
            "Custom Upload Temperature Profile"
        )
        st.altair_chart(upload_chart, use_container_width=True)

    # Display contact info
    display_contact()

if __name__ == "__main__":
    main()
