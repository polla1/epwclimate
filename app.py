# app.py
import streamlit as st
import pandas as pd
import altair as alt
from database import load_baseline, load_2050, load_2080, read_epw
from sidebar import display_sidebar
from contact import display_contact

# Set up color scheme
SCENARIO_COLORS = {
    '2023 Baseline': 'green',
    '2050 Projection': 'blue',
    '2080 Projection': 'red'
}

def create_simple_chart(data, title):
    """Create an easy-to-read temperature chart"""
    melted_data = data.reset_index().melt(
        id_vars=['DateTime'],
        var_name='Scenario',
        value_name='Temperature'
    )
    
    chart = alt.Chart(melted_data).mark_line().encode(
        x='DateTime:T',
        y='Temperature:Q',
        color='Scenario:N',
        tooltip=['Scenario', 'Temperature']
    ).properties(
        title=title,
        height=400
    )
    return chart

def main():
    # Basic page setup
    st.set_page_config(page_title="Climate App", layout="wide")
    st.title("Simple Climate Visualizer")
    
    # Load main data
    try:
        baseline = load_baseline().rename(columns={'Temperature': '2023 Baseline'})
        proj2050 = load_2050().rename(columns={'Temperature': '2050 Projection'})
        proj2080 = load_2080().rename(columns={'Temperature': '2080 Projection'})
        main_data = pd.concat([baseline, proj2050, proj2080], axis=1)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return

    # Scenario selection
    st.header("Choose Scenarios")
    selected_scenarios = st.multiselect(
        "Which scenarios would you like to see?",
        options=list(SCENARIO_COLORS.keys()),
        default=list(SCENARIO_COLORS.keys())
    )

    # Show main chart
    if selected_scenarios:
        st.altair_chart(
            create_simple_chart(
                main_data[selected_scenarios],
                "Temperature Over Time"
            ),
            use_container_width=True
        )
    else:
        st.warning("Please select at least one scenario")

    # File upload section
    st.header("Upload Your Own Data")
    uploaded_files = display_sidebar()
    
    if uploaded_files:
        for file in uploaded_files:
            try:
                uploaded_data = read_epw(file)
                st.write(f"Showing data for: {file.name}")
                st.line_chart(uploaded_data['Temperature'])
            except Exception as e:
                st.error(f"Error with {file.name}: {str(e)}")

    # Monthly analysis
    st.header("Monthly View")
    selected_month = st.selectbox(
        "Choose a month",
        options=list(range(1, 13)),
        format_func=lambda x: pd.Timestamp(2023, x, 1).strftime('%B')
    )
    
    monthly_data = main_data[main_data.index.month == selected_month]
    if not monthly_data.empty:
        st.write(f"Temperature data for {pd.Timestamp(2023, selected_month, 1).strftime('%B')}")
        st.line_chart(monthly_data)
    else:
        st.warning("No data available for selected month")

    # Contact information
    display_contact()

if __name__ == "__main__":
    main()
