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
    # [Keep all your original Erbil analysis code here]
    # This function remains unchanged from your working version

def show_epw_analysis():
    # [Keep all your original EPW analysis code here]
    # This function remains unchanged from your working version

def main():
    st.set_page_config(page_title="Climate Analysis", layout="wide")
    
    # Enhanced tab styling
    st.markdown("""
    <style>
        div[data-testid="stTabs"] {
            background: linear-gradient(145deg, #f8f9fa, #ffffff);
            padding: 12px;
            border-radius: 15px;
            margin: 20px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        button[data-testid="baseButton-header"] {
            font-size: 18px !important;
            font-weight: 600 !important;
            padding: 16px 32px !important;
            margin: 0 6px !important;
            border-radius: 12px !important;
            transition: all 0.3s ease !important;
            border: 2px solid transparent !important;
        }
        
        button[data-testid="baseButton-header"][aria-selected="true"] {
            background: linear-gradient(135deg, #2c3e50, #3498db) !important;
            color: white !important;
            border-color: #ffffff !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.15);
            transform: scale(1.05);
        }
        
        button[data-testid="baseButton-header"]:hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        }
        
        button[data-testid="baseButton-header"][aria-selected="false"] {
            background: #e9ecef !important;
            color: #495057 !important;
            border-color: #dee2e6 !important;
        }
        
        .stTabs > div > div:not(:last-child) {
            border-right: 2px solid #dee2e6;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🌡️ Climate Analysis Dashboard")
    
    erbil_data = load_erbil_data()
    
    tab1, tab2 = st.tabs([
        "🌍 Erbil Projections", 
        "📤 Custom EPW Analysis"
    ])
    
    with tab1:
        show_erbil_analysis(erbil_data)
    
    with tab2:
        show_epw_analysis()
    
    display_contact()
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<center> Polla Sktani ©2025 </center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
