import streamlit as st
import pandas as pd
import altair as alt
from database import load_baseline, load_2050, load_2080, read_epw

# Color configuration
SCENARIO_COLORS = {
    '2023 Baseline': '#00FF00',  # Green
    '2050 Projection': '#0000FF',  # Blue
    '2080 Projection': '#FF0000'  # Red
}

def create_chart(data, colors, title):
    """Create interactive line chart with proper formatting"""
    try:
        melted = data.reset_index().melt(
            id_vars=['DateTime'],
            var_name='Scenario',
            value_name='Temperature'
        )
        
        chart = alt.Chart(melted).mark_line(opacity=0.7).encode(
            x=alt.X('DateTime:T', title='Date', axis=alt.Axis(format='%b %d')),
            y=alt.Y('Temperature:Q', title='Temperature (°C)'),
            color=alt.Color('Scenario:N').scale(
                domain=list(colors.keys()),
                range=list(colors.values())
            ),
            tooltip=[
                alt.Tooltip('DateTime:T', title='Date', format='%B %d, %Y'),
                'Scenario',
                alt.Tooltip('Temperature:Q', format='.1f°C')
            ]
        ).properties(
            height=400,
            title=title
        )
        return chart
    except Exception as e:
        st.error(f"Chart creation failed: {str(e)}")
        return None

def display_sidebar():
    """File upload sidebar component"""
    with st.sidebar:
        st.header("Upload Custom Data")
        return st.file_uploader(
            "Choose EPW files",
            type="epw",
            accept_multiple_files=True
        )

def main():
    # Page configuration
    st.set_page_config(page_title="Climate Analysis", layout="wide")
    st.title("Erbil Climate Scenarios Visualization")
    
    # Load core data
    try:
        baseline = load_baseline().rename(columns={'Temperature': '2023 Baseline'})
        proj2050 = load_2050().rename(columns={'Temperature': '2050 Projection'})
        proj2080 = load_2080().rename(columns={'Temperature': '2080 Projection'})
        
        erbil_data = pd.concat([baseline, proj2050, proj2080], axis=1).dropna()
        
        if erbil_data.empty:
            st.error("No data loaded - check EPW files")
            st.stop()
    except Exception as e:
        st.error(f"Data loading error: {str(e)}")
        st.stop()
    
    # File upload handling
    uploaded_files = display_sidebar()
    custom_data = {}
    
    if uploaded_files:
        for file in uploaded_files:
            try:
                df = read_epw(file)
                custom_data[file.name] = df['Temperature']
            except Exception as e:
                st.error(f"Error processing {file.name}: {str(e)}")

    # Scenario selection
    st.header("Select Climate Scenarios")
    selected_scenarios = []
    cols = st.columns(3)
    
    for i, scenario in enumerate(SCENARIO_COLORS):
        with cols[i]:
            if st.checkbox(scenario, value=True, key=f"scenario_{i}"):
                selected_scenarios.append(scenario)

    # Main visualization
    if selected_scenarios:
        st.altair_chart(
            create_chart(
                erbil_data[selected_scenarios],
                {k: SCENARIO_COLORS[k] for k in selected_scenarios},
                "Erbil Temperature Projections Comparison"
            ),
            use_container_width=True
        )
    else:
        st.warning("Please select at least one scenario")

    # Custom uploads display
    if custom_data:
        st.header("Custom Upload Analysis")
        try:
            custom_df = pd.concat(custom_data.values(), axis=1)
            custom_df.columns = custom_data.keys()
            
            st.altair_chart(
                create_chart(
                    custom_df,
                    {name: '#FFA500' for name in custom_data},
                    "Uploaded Temperature Data"
                ),
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Couldn't display uploads: {str(e)}")

    # Monthly analysis
    st.header("Monthly Temperature Breakdown")
    month = st.selectbox(
        "Select Month for Detailed View",
        options=range(1, 13),
        format_func=lambda x: pd.Timestamp(2023, x, 1).strftime('%B')
    )
    
    try:
        monthly_data = erbil_data[erbil_data.index.month == month]
        if not monthly_data.empty:
            st.altair_chart(
                create_chart(
                    monthly_data,
                    SCENARIO_COLORS,
                    f"{pd.Timestamp(2023, month, 1).strftime('%B')} Daily Temperatures"
                ),
                use_container_width=True
            )
        else:
            st.warning("No data available for selected month")
    except Exception as e:
        st.error(f"Monthly analysis failed: {str(e)}")

# ====== CRITICAL FIX ======
if __name__ == "__main__":
    main()
