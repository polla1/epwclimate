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

def show_erbil_analysis(erbil_data):
    """Content for Erbil projections tab"""
    # [Keep the exact same Erbil analysis code from previous version]

def show_epw_analysis():
    """Content for custom EPW analysis tab with integrated file upload"""
    st.header("Custom EPW Analysis")
    
    # File uploader inside the EPW tab
    with st.container():
        st.subheader("📤 Upload EPW Files")
        uploaded_files = st.file_uploader(
            "Select EPW weather files",
            type="epw",
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        
        if uploaded_files:
            st.success(f"{len(uploaded_files)} file(s) selected:")
            for file in uploaded_files:
                st.write(f"- {file.name}")
            
            if st.button("Clear Files", key="epw_clear"):
                st.experimental_rerun()
    
    # Analysis section
    if uploaded_files:
        try:
            epw_dfs = []
            for idx, file in enumerate(uploaded_files):
                epw_data = read_epw(file)
                epw_data = epw_data.rename(columns={'Temperature': f'Custom {idx+1}'})
                epw_dfs.append(epw_data)
            
            combined_epw = pd.concat(epw_dfs, axis=1)
            
            # Visualization
            st.altair_chart(
                create_chart(
                    combined_epw,
                    {col: '#8A2BE2' for col in combined_epw.columns},
                    "EPW Temperature Analysis",
                    x_axis='DateTime:T',
                    x_format='%B'
                ), use_container_width=True
            )
            
            # Data preview
            if st.checkbox("Show raw data preview", key="epw_preview"):
                st.dataframe(combined_epw.head())

        except Exception as e:
            st.error(f"EPW Processing Error: {str(e)}")
            st.markdown("""
            **Required Format:**
            - Valid EPW file structure
            - Contains temperature data column
            - Proper datetime formatting
            """)
    else:
        st.info("Please upload EPW files above to begin analysis")

def main():
    st.set_page_config(page_title="Climate Analysis", layout="wide")
    st.title("🌡️ Climate Analysis Dashboard")
    
    # Load Erbil data
    erbil_data = load_erbil_data()
    
    # Create tabs
    tab1, tab2 = st.tabs(["Erbil Projections", "Custom EPW Analysis"])
    
    with tab1:
        show_erbil_analysis(erbil_data)
    
    with tab2:
        show_epw_analysis()  # No need to pass uploaded_files
    
    # Footer
    display_contact()
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<center> Polla Sktani ©2025 </center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
