import streamlit as st
import pandas as pd
import altair as alt
from database import load_baseline, load_2050, load_2080, read_epw, count_hours_above_threshold
from sidebar import display_sidebar
from contact import display_contact

def main():
    # THIS MUST BE THE FIRST STREAMLIT COMMAND
    st.set_page_config(page_title="Climate Analysis", layout="wide")
    
    # Now add other Streamlit components
    st.title("🌡️ Erbil Climate Projections")
    
    # Move CSS here
    st.markdown("""
    <style>
        .gradient-slider div[data-baseweb="slider"] > div { 
            background: linear-gradient(90deg, #90EE90 0%, #FFA500 50%, #FF4500 100%);
            height: 8px;
            border-radius: 4px;
        }
        .severity-box {
            text-align: center; 
            padding: 8px; 
            border-radius: 5px; 
            width: 32%;
            margin: 5px 0;
            transition: background-color 0.2s;
        }
    </style>
    """, unsafe_allow_html=True)

    # Rest of your code remains the same...
    ERBIL_COLORS = {
        '2023 Baseline': '#00FF00',
        '2050 Projection': '#0000FF',
        '2080 Projection': '#FF0000'
    }

    # Rest of the original code...

if __name__ == "__main__":
    main()
