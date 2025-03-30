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
    """Create a line chart with month-only x-axis"""
    # Prepare data with proper month names
    df_melted = data.reset_index().melt(
        id_vars=['DateTime'],
        var_name='Scenario',
        value_name='Temperature'
    )
    
    # Add formatted month column
    df_melted['Month'] = df_melted['DateTime'].dt.strftime('%B')
    
    # Define month order for correct sorting
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # Create chart with explicit month ordering
    chart = alt.Chart(df_melted).mark_line(
        opacity=0.7,
        strokeWidth=2
    ).encode(
        x=alt.X('Month:N', title='Month', 
               sort=month_order,
               axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Temperature:Q', title='Temperature (°C)'),
        color=alt.Color('Scenario:N').scale(
            domain=list(colors.keys()),
            range=list(colors.values())
        ),
        tooltip=[
            alt.Tooltip('DateTime:T', title='Date', format='%B %Y'),
            'Scenario',
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
    return pd.concat([
        load_baseline().rename(columns={'Temperature': '2023 Baseline'}),
        load_2050().rename(columns={'Temperature': '2050 Projection'}),
        load_2080().rename(columns={'Temperature': '2080 Projection'})
    ], axis=1)

def main():
    st.set_page_config(page_title="Climate Analysis", layout="wide")
    st.title("Climate Data Visualization")
    
    # Load Erbil data
    erbil_data = load_erbil_data()
    
    # Handle uploaded files
    uploaded_files = display_sidebar()
    custom_data = {}
    for file in uploaded_files:
        custom_data[file.name] = read_epw(file)['Temperature']

    # Scenario selection
    st.header("Weather file (.EPW) Scenarios of Erbil")
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
                "Temperature Projections Comparison"
            ),
            use_container_width=True
        )
    else:
        st.warning("Please select at least one Erbil scenario")

    # Custom uploads
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

    # Monthly analysis
    st.header("Monthly Temperature Analysis (Erbil)")
    month = st.selectbox(
        "Select Month", 
        range(1, 13), 
        format_func=lambda x: pd.Timestamp(2023, x, 1).strftime('%B'),
        key="month_select"
    )
    
    monthly_data = erbil_data[erbil_data.index.month == month]
    st.line_chart(
        monthly_data,
        use_container_width=True
    )

    display_contact()

if __name__ == "__main__":
    main()
