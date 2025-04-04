import streamlit as st
import pandas as pd
import altair as alt
from database import load_baseline, load_2050, load_2080, read_epw, count_hours_above_threshold
from sidebar import display_sidebar
from contact import display_contact

ERBIL_COLORS = {
    '2023 Baseline': '#00FF00',
    '2050 Projection': '#0000FF',
    '2080 Projection': '#FF0000'
}

def create_chart(data, colors, title, x_axis='DateTime:T', x_format='%B'):
    df_melted = data.reset_index().melt(
        id_vars=['DateTime'],
        var_name='Scenario',
        value_name='Temperature'
    )
    return alt.Chart(df_melted).mark_line(
        opacity=0.7,
        strokeWidth=2
    ).encode(
        x=alt.X(x_axis, title='Month', axis=alt.Axis(format=x_format)),
        y=alt.Y('Temperature:Q', title='Temperature (°C)'),
        color=alt.Color('Scenario:N').scale(
            domain=list(colors.keys()),
            range=list(colors.values())
        ),
        tooltip=['Scenario', 'DateTime', alt.Tooltip('Temperature:Q', format='.1f')]
    ).properties(
        height=400,
        title=title
    )

@st.cache_data
def load_erbil_data():
    return pd.concat([
        load_baseline().rename(columns={'Temperature': '2023 Baseline'}),
        load_2050().rename(columns={'Temperature': '2050 Projection'}),
        load_2080().rename(columns={'Temperature': '2080 Projection'})
    ], axis=1)

def show_erbil_analysis():
    """Main page with original 3 charts"""
    erbil_data = load_erbil_data()
    
    # ===== Chart 1: Scenarios =====
    st.markdown("### 🌍 Climate Scenario Comparison")
    selected_erbil = []
    cols = st.columns(3)
    for i, scenario in enumerate(ERBIL_COLORS):
        with cols[i]:
            if st.checkbox(scenario, value=True, key=f"erbil_{i}"):
                selected_erbil.append(scenario)
    
    if selected_erbil:
        st.altair_chart(
            create_chart(
                erbil_data[selected_erbil],
                {k: v for k, v in ERBIL_COLORS.items() if k in selected_erbil},
                "Temperature Projections Over Time"
            ), use_container_width=True)
    else:
        st.warning("Please select at least one scenario")

    # ===== Chart 2: Monthly Analysis =====
    st.markdown("### 📅 Monthly Temperature Patterns")
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
                f"Hourly Temperatures in {pd.Timestamp(2023, month, 1).strftime('%B')}",
                x_axis='DateTime:T',
                x_format='%d'
            ), use_container_width=True)
    else:
        st.warning("No data for selected month")

    # ===== Chart 3: Extreme Heat Analysis =====
    st.markdown("### 🔥 Extreme Heat Analysis")
    # ... keep existing extreme heat analysis code ...

def show_custom_epw_analysis():
    """New page for custom EPW file analysis"""
    st.markdown("## 📤 Custom EPW Analysis")
    
    with st.sidebar:
        st.header("EPW Upload")
        uploaded_files = st.file_uploader(
            "Upload EPW weather files",
            type="epw",
            accept_multiple_files=True,
            help="Upload one or more EPW files for analysis"
        )
    
    if uploaded_files:
        try:
            custom_data = pd.concat([read_epw(file) for file in uploaded_files], axis=1)
            custom_data.columns = [f"Custom {i+1}" for i in range(len(uploaded_files))]
            
            st.markdown("### 🌡️ Custom Temperature Analysis")
            st.altair_chart(
                create_chart(
                    custom_data,
                    {'Custom Scenario': '#8A2BE2'},  # Purple color
                    "Custom EPW Temperature Data",
                    x_axis='DateTime:T',
                    x_format='%B'
                ), use_container_width=True
            )
            
            # Add custom analysis specific to EPW files
            st.markdown("### 📈 Custom Statistics")
            # Add your custom statistics/analysis here
            
        except Exception as e:
            st.error(f"Error processing EPW files: {str(e)}")
    else:
        st.info("Please upload EPW files using the sidebar")

def main():
    st.set_page_config(page_title="Climate Analysis", layout="wide")
    
    # Page selection in sidebar
    st.sidebar.markdown("## Navigation")
    page = st.sidebar.radio(
        "Choose Analysis",
        ["Erbil Climate Projections", "Custom EPW Analysis"],
        label_visibility="collapsed"
    )
    
    # Page title
    st.title("🌡️ " + page)
    
    # Show selected page
    if page == "Erbil Climate Projections":
        show_erbil_analysis()
    else:
        show_custom_epw_analysis()
    
    # Common footer
    display_contact()
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<center> Polla Sktani ©2025 </center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
