import streamlit as st
import pandas as pd
import altair as alt
from database import load_baseline, load_2050, load_2080, read_epw

# Color settings for scenarios
SCENARIO_COLORS = {
    '2023 Baseline': '#00FF00',  # Green
    '2050 Projection': '#0000FF',  # Blue
    '2080 Projection': '#FF0000'  # Red
}

def create_chart(data, colors, title):
    """Create an interactive temperature chart"""
    try:
        melted = data.reset_index().melt(id_vars=['DateTime'], 
                                        var_name='Scenario', 
                                        value_name='Temperature')
        
        return alt.Chart(melted).mark_line(opacity=0.7).encode(
            x=alt.X('DateTime:T', title='Date', axis=alt.Axis(format='%b %d')),
            y=alt.Y('Temperature:Q', title='Temperature (°C)'),
            color=alt.Color('Scenario:N').scale(domain=list(colors.keys()), 
                                            range=list(colors.values())),
            tooltip=['DateTime:T', 'Scenario', alt.Tooltip('Temperature:Q', format='.1f°C')]
        ).properties(
            height=400,
            title=title
        )
    except Exception as e:
        st.error(f"Chart error: {str(e)}")
        return None

def sidebar():
    """File upload sidebar"""
    with st.sidebar:
        st.header("Upload Custom EPW Files")
        uploaded_files = st.file_uploader(
            "Choose EPW files",
            type="epw",
            accept_multiple_files=True
        )
        return uploaded_files

def main():
    # Page setup
    st.set_page_config(page_title="Erbil Climate", layout="wide")
    st.title("Erbil Climate Scenarios Visualization")
    
    # Load base data
    try:
        baseline = load_baseline().rename(columns={'Temperature': '2023 Baseline'})
        proj2050 = load_2050().rename(columns={'Temperature': '2050 Projection'})
        proj2080 = load_2080().rename(columns={'Temperature': '2080 Projection'})
        
        # Combine data ensuring same index
        erbil_data = pd.concat([baseline, proj2050, proj2080], axis=1).dropna()
        
    except Exception as e:
        st.error(f"Data loading failed: {str(e)}")
        st.stop()

    # Show sidebar
    uploaded_files = sidebar()

    # Process uploaded files
    custom_data = {}
    if uploaded_files:
        for file in uploaded_files:
            try:
                df = read_epw(file)
                custom_data[file.name] = df['Temperature']
            except Exception as e:
                st.error(f"Error processing {file.name}: {str(e)}")

    # Scenario selection
    st.header("Select Scenarios")
    selected = []
    cols = st.columns(3)
    for i, scenario in enumerate(SCENARIO_COLORS):
        with cols[i]:
            if st.checkbox(scenario, value=True, key=f"scen_{i}"):
                selected.append(scenario)

    # Main chart
    if selected:
        st.altair_chart(
            create_chart(erbil_data[selected], 
                       {k: SCENARIO_COLORS[k] for k in selected},
                       "Temperature Projections for Erbil"),
            use_container_width=True
        )
    else:
        st.warning("Please select at least one scenario")

    # Show uploaded files
    if custom_data:
        st.header("Uploaded Data")
        custom_df = pd.concat(custom_data.values(), axis=1)
        st.altair_chart(
            create_chart(custom_df, 
                        {name: '#FFA500' for name in custom_data.keys()},
                        "Custom Uploaded Data"),
            use_container_width=True
        )

    # Monthly analysis
    st.header("Monthly Analysis")
    month = st.selectbox("Select Month", range(1,13), 
                        format_func=lambda x: pd.Timestamp(2023, x, 1).strftime('%B'))
    
    monthly_data = erbil_data[erbil_data.index.month == month]
    if not monthly_data.empty:
        st.altair_chart(
            create_chart(monthly_data, SCENARIO_COLORS,
                        f"{pd.Timestamp(2023, month, 1).strftime('%B')} Daily Temperatures"),
            use_container_width=True
        )

if __name__ ==
