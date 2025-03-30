import streamlit as st
import pandas as pd
import altair as alt
from database import load_baseline, load_2050, load_2080, read_epw
from sidebar import display_sidebar
from contact import display_contact

# Debug mode
DEBUG = True  # Set to False for production

ERBIL_COLORS = {
    '2023 Baseline': '#00FF00',
    '2050 Projection': '#0000FF',
    '2080 Projection': '#FF0000'
}

def debug_info(data, name):
    """Show debug information about data"""
    if DEBUG:
        with st.expander(f"Debug: {name}"):
            st.write(f"Shape: {data.shape}")
            st.write("First 5 rows:", data.head())
            st.write("Index type:", type(data.index))
            st.write("Columns:", data.columns.tolist())

def create_chart(data, colors, title):
    """Create chart with data validation"""
    if data.empty:
        st.warning(f"No data to display for {title}")
        return None
        
    try:
        df_melted = data.reset_index().melt(
            id_vars=['DateTime'],
            var_name='Scenario',
            value_name='Temperature'
        )
        
        chart = alt.Chart(df_melted).mark_line(
            opacity=0.7,
            strokeWidth=2
        ).encode(
            x=alt.X('DateTime:T', title='Date', axis=alt.Axis(format='%b %d')),
            y=alt.Y('Temperature:Q', title='Temperature (°C)', scale=alt.Scale(zero=False)),
            color=alt.Color('Scenario:N').scale(
                domain=list(colors.keys()),
                range=list(colors.values())
            ),
            tooltip=['Scenario', alt.Tooltip('Temperature:Q', format='.1f°C')]
        ).properties(
            height=400,
            title=title
        )
        
        debug_info(df_melted, title)
        return chart
        
    except Exception as e:
        st.error(f"Chart error: {str(e)}")
        return None

@st.cache_data
def load_erbil_data():
    """Load data with validation"""
    try:
        baseline = load_baseline().rename(columns={'Temperature': '2023 Baseline'})
        proj2050 = load_2050().rename(columns={'Temperature': '2050 Projection'})
        proj2080 = load_2080().rename(columns={'Temperature': '2080 Projection'})

        # Validate data
        if any(df.empty for df in [baseline, proj2050, proj2080]):
            st.error("Missing scenario data files!")
            st.stop()

        combined = pd.concat([baseline, proj2050, proj2080], axis=1)
        debug_info(combined, "Combined Data")
        return combined
        
    except Exception as e:
        st.error(f"Data loading failed: {str(e)}")
        st.stop()

def main():
    st.set_page_config(page_title="Climate Analysis", layout="wide")
    st.title("Climate Data Visualization")
    
    # Load data
    erbil_data = load_erbil_data()
    
    # File uploads
    uploaded_files = display_sidebar()
    custom_data = {}
    
    for file in uploaded_files:
        try:
            df = read_epw(file)
            if not df.empty and 'Temperature' in df.columns:
                custom_data[file.name] = df['Temperature']
                debug_info(df, f"Uploaded: {file.name}")
            else:
                st.error(f"Invalid data in {file.name}")
        except Exception as e:
            st.error(f"Error processing {file.name}: {str(e)}")

    # Main scenarios
    st.header("Weather file (.EPW) Scenarios of Erbil")
    
    selected_scenarios = []
    cols = st.columns(3)
    for i, scenario in enumerate(ERBIL_COLORS):
        with cols[i]:
            if st.checkbox(scenario, value=True, key=f"scen_{i}"):
                selected_scenarios.append(scenario)

    if selected_scenarios:
        chart = create_chart(
            erbil_data[selected_scenarios],
            {k: ERBIL_COLORS[k] for k in selected_scenarios},
            "Interactive Yearly Temperature Projections"
        )
        if chart:
            st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("Please select at least one scenario")

    # Uploads
    if custom_data:
        st.header("Uploaded Climate Files")
        try:
            custom_df = pd.concat(custom_data.values(), axis=1)
            custom_df.columns = custom_data.keys()
            
            upload_chart = create_chart(
                custom_df,
                {name: '#FFA500' for name in custom_data},
                "Uploaded Temperature Data Comparison"
            )
            if upload_chart:
                st.altair_chart(upload_chart, use_container_width=True)
        except Exception as e:
            st.error(f"Error displaying uploads: {str(e)}")

    # Monthly analysis
    st.header("Monthly Temperature Analysis")
    month = st.selectbox(
        "Select Month", 
        range(1, 13), 
        format_func=lambda x: pd.Timestamp(2023, x, 1).strftime('%B'),
        key="month_select"
    )
    
    try:
        monthly_data = erbil_data[erbil_data.index.month == month]
        if not monthly_data.empty:
            monthly_chart = create_chart(
                monthly_data,
                ERBIL_COLORS,
                f"{pd.Timestamp(2023, month, 1).strftime('%B')} Daily Temperatures"
            )
            if monthly_chart:
                st.altair_chart(monthly_chart, use_container_width=True)
        else:
            st.warning("No data available for selected month")
    except Exception as e:
        st.error(f"Monthly analysis error: {str(e)}")

    display_contact()

if __name__ == "__main__":
    main()
