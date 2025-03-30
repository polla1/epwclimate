import streamlit as st
import pandas as pd
import altair as alt
from database import load_baseline, load_2050, load_2080, read_epw
from sidebar import display_sidebar
from contact import display_contact

def create_transparent_chart(data):
    """Create a line chart with semi-transparent lines"""
    # Melt dataframe for Altair
    df_melted = data.reset_index().melt(
        id_vars=['DateTime'],
        var_name='Scenario',
        value_name='Temperature'
    )
    
    # Create base chart
    base = alt.Chart(df_melted).encode(
        x=alt.X('DateTime:T', title='Date'),
        y=alt.Y('Temperature:Q', title='Temperature (°C)'),
        color='Scenario:N'
    )
    
    # Create line chart with transparency
    chart = base.mark_line(
        opacity=0.6,
        strokeWidth=2
    ).properties(
        height=400,
        width=800
    )
    
    return chart

@st.cache_data
def load_all_data():
    """Load and cache all baseline climate data"""
    return {
        '2023': load_baseline(),
        '2050': load_2050(),
        '2080': load_2080()
    }

def main():
    st.set_page_config(page_title="Erbil Climate Analysis", layout="wide")
    st.title("Erbil City Temperature Analysis")
    
    # Load core datasets
    data = load_all_data()
    
    # Combine baseline data
    combined = pd.concat([
        data['2023'].rename(columns={'Temperature': '2023 Baseline'}),
        data['2050'].rename(columns={'Temperature': '2050 Projection'}),
        data['2080'].rename(columns={'Temperature': '2080 Projection'})
    ], axis=1)

    # Handle uploaded files
    uploaded_files = display_sidebar()
    for file in uploaded_files:
        temp_df = read_epw(file)
        combined[file.name] = temp_df['Temperature']

    # Yearly Comparison Section
    st.header("Interactive Yearly Temperature Comparison")
    
    # Scenario toggle controls
    col1, col2, col3 = st.columns(3)
    with col1:
        show_2023 = st.checkbox("2023 Baseline", value=True, key="y2023")
    with col2:
        show_2050 = st.checkbox("2050 Projection", value=True, key="y2050")
    with col3:
        show_2080 = st.checkbox("2080 Projection", value=True, key="y2080")

    # Filter columns based on selections
    selected = []
    if show_2023: selected.append('2023 Baseline')
    if show_2050: selected.append('2050 Projection')
    if show_2080: selected.append('2080 Projection')
    
    # Add uploaded files to selection
    if uploaded_files:
        st.subheader("Custom Uploads")
        upload_cols = st.columns(2)
        for idx, file in enumerate(uploaded_files):
            with upload_cols[idx%2]:
                if st.checkbox(file.name, value=True, key=f"upload_{idx}"):
                    selected.append(file.name)

    # Display chart or warning
    if selected:
        chart_data = combined[selected]
        st.altair_chart(
            create_transparent_chart(chart_data),
            use_container_width=True
        )
    else:
        st.warning("Please select at least one scenario to display")

    # Monthly Analysis Section
    st.header("Monthly Temperature Analysis")
    month = st.selectbox(
        "Select Month", 
        range(1, 13), 
        format_func=lambda x: pd.Timestamp(2023, x, 1).strftime('%B'),
        key="month_select"
    )
    
    monthly_data = combined[combined.index.month == month]
    st.line_chart(
        monthly_data,
        use_container_width=True
    )

    display_contact()

if __name__ == "__main__":
    main()
