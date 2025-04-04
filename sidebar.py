import streamlit as st
from datetime import datetime

def display_sidebar():
    """Enhanced sidebar with better visual design"""
    
    st.sidebar.markdown("""
    <style>
        .sidebar-header {
            color: #2c3e50;
            font-size: 24px !important;
            font-weight: bold;
            margin-bottom: 15px;
        }
        .sidebar-section {
            padding: 10px;
            background: #f8f9fa;
            border-radius: 8px;
            margin: 10px 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # Main Header
    st.sidebar.markdown('<div class="sidebar-header">🌡️ Climate Analysis Toolkit</div>', unsafe_allow_html=True)
    
    # Data Sources Section
    with st.sidebar.expander("📂 Data Sources", expanded=True):
        st.markdown("""
        - **Erbil Projections**:
          - 2023 Baseline
          - 2050 Scenario
          - 2080 Scenario
        - **Custom Data**:
          - EPW weather files
        """)
    
    # Analysis Features
    st.sidebar.markdown('---')
    st.sidebar.markdown('### 🔍 Analysis Tools')
    st.sidebar.markdown("""
    - Temperature Trends
    - Monthly Patterns
    - Extreme Heat Analysis
    - Custom Comparisons
    """)
    
    # Quick Guide
    with st.sidebar.expander("ℹ️ Quick Guide"):
        st.markdown("""
        1. Select scenarios using checkboxes
        2. Choose month for detailed view
        3. Adjust temperature threshold
        4. Upload EPW files for custom analysis
        """)
    
    # Version & Author
    st.sidebar.markdown('---')
    st.sidebar.caption(f"""
    <div style="color: #7f8c8d; font-size: 0.8em">
        Version: 1.1.0<br>
        Last update: {datetime.now().strftime('%Y-%m-%d')}<br>
        Developed by Polla Sktani
    </div>
    """, unsafe_allow_html=True)
