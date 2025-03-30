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
    
    # Custom axis formatting
    if "Yearly" in title:
        x_axis = alt.X('DateTime:T', title='Month', 
                      axis=alt.Axis(format='%b', labelAngle=0))
    else:
        x_axis = alt.X('DateTime:T', title='Date')
    
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
        tooltip=['Scenario', alt.Tooltip('Temperature:Q', format='.1f')]
    ).properties(
        height=400,
        title=title
    )

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
    
    # Load core data
    erbil_data = load_erbil_data()
    
    # Handle uploads
    uploaded_files = display_sidebar()
    custom_data = {}
    for file in uploaded_files:
        temp_df = read_epw(file)
        custom_data[file.name] = temp_df['Temperature']

    # =====================
    # Erbil Yearly Analysis
    # =====================
    st.header("Weather file (.EPW) Scenarios of Erbil")
    
    selected_erbil = []
    cols = st.columns(3)
    for i, col in enumerate(cols):
        with col:
            scenario = list(ERBIL_COLORS.keys())[i]
            if st.checkbox(scenario, value=True, key=f"erbil_{i}"):
                selected_erbil.append(scenario)
    
    if selected_erbil:
        st.altair_chart(
            create_chart(
                erbil_data[selected_erbil],
                {k: ERBIL_COLORS[k] for k in selected_erbil},
                "Interactive Yearly Temperature of 2023, 2050, and 2080 - Erbil, Iraq"
            ),
            use_container_width=True
        )
    else:
        st.warning("Please select at least one Erbil scenario")

    # ======================
    # Custom Uploads Section
    # ======================
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

 # =====================
# Monthly Analysis (Fixed)
# =====================
st.header("Monthly Temperature Analysis (Erbil)")
month = st.selectbox(
    "Select Month", 
    range(1, 13), 
    format_func=lambda x: pd.Timestamp(2023, x, 1).strftime('%B'),
    key="month_select"
)

# Process monthly data
if not erbil_data.empty:
    # Filter by month and resample to daily
    monthly_data = erbil_data[erbil_data.index.month == month]
    daily_data = monthly_data.resample('D').mean()
    
    # Melt for Altair
    melted_data = daily_data.reset_index().melt(
        id_vars=['DateTime'],
        var_name='Scenario',
        value_name='Temperature'
    )
    
    # Create chart
    monthly_chart = alt.Chart(melted_data).mark_line().encode(
        x=alt.X('DateTime:T', title='Day of Month', 
               axis=alt.Axis(format='%-d', labelFlush=True)),
        y=alt.Y('Temperature:Q', title='Temperature (°C)',
               scale=alt.Scale(zero=False)),
        color=alt.Color('Scenario:N').scale(
            domain=list(ERBIL_COLORS.keys()),
            range=list(ERBIL_COLORS.values())
        ),
        tooltip=[
            alt.Tooltip('DateTime:T', title='Date', format='%b %-d'),
            alt.Tooltip('Temperature:Q', format='.1f°C'),
            'Scenario'
        ]
    ).properties(
        width=800,
        title=f"{pd.Timestamp(2023, month, 1).strftime('%B')} Daily Temperatures"
    )
    
    st.altair_chart(monthly_chart, use_container_width=True)
else:
    st.warning("No data available for selected month")

    display_contact()

if __name__ == "__main__":
    main()
