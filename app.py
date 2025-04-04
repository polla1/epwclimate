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

def main():
    st.set_page_config(page_title="Climate Analysis", layout="wide")
    st.title("🌡️ Erbil Climate Projections")
    
    # Load data
    erbil_data = load_erbil_data()
    
    # Initialize uploaded_files with empty list
    uploaded_files = []
    try:
        uploaded_files = display_sidebar()
    except Exception as e:
        st.error(f"Sidebar error: {str(e)}")
    
    # ===== Original Erbil Charts =====
    # [Keep all your original chart code here - 100% unchanged]
    
    # ===== Fixed EPW Handling =====
    if uploaded_files:  # Now properly defined
        with st.expander("📤 EPW File Analysis", expanded=True):
            try:
                # Column handling with fallbacks
                DT_COLS = ['datetime', 'date/time', 'date', 'timestamp']
                TEMP_COLS = ['dry bulb temperature', 'temperature', 'temp']
                
                epw_dfs = []
                valid_files = 0
                
                for idx, file in enumerate(uploaded_files):
                    df = read_epw(file)
                    df.columns = df.columns.str.lower().str.strip()
                    
                    # Find datetime column
                    dt_col = next((col for col in DT_COLS if col in df.columns), None)
                    if not dt_col:
                        continue
                    
                    # Find temperature column
                    temp_col = next((col for col in TEMP_COLS if col in df.columns), None)
                    if not temp_col:
                        continue
                    
                    # Process valid file
                    try:
                        epw_df = df[[dt_col, temp_col]].copy()
                        epw_df.columns = ['DateTime', f'EPW {idx+1}']
                        epw_df['DateTime'] = pd.to_datetime(epw_df['DateTime'])
                        epw_dfs.append(epw_df.set_index('DateTime'))
                        valid_files += 1
                    except Exception as e:
                        continue
                
                if valid_files > 0:
                    combined_epw = pd.concat(epw_dfs, axis=1)
                    st.altair_chart(
                        create_chart(
                            combined_epw,
                            {col: '#8A2BE2' for col in combined_epw.columns},
                            "EPW Temperature Analysis"
                        ), use_container_width=True
                    )
                
            except Exception as e:
                st.error(f"EPW error: {str(e)}")

    # Footer 
    display_contact()
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<center> Polla Sktani ©2025 </center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
