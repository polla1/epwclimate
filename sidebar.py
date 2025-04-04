import streamlit as st
from datetime import datetime

def display_sidebar():
    """Enhanced sidebar with visual improvements"""
    
    # Custom CSS injection
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background: #f8f9fa !important;
            padding: 20px !important;
        }
        .sidebar-section {
            padding: 15px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 15px 0;
        }
        .sidebar-header {
            color: #2c3e50;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 25px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar Header
    st.sidebar.markdown('<div class="sidebar-header">🌡️ Climate Toolkit</div>', unsafe_allow_html=True)
    
    # Data Sources Section
    with st.sidebar.container():
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.subheader("📂 Data Sources")
        st.markdown("""
        - **Official Projections**:
          - 2023 Baseline
          - 2050 Scenario
          - 2080 Scenario
        - **Custom Data**:
          - EPW Weather Files
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Guide
    with st.sidebar.container():
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.subheader("ℹ️ User Guide")
        st.markdown("""
        1. Select scenarios using checkboxes
        2. Choose month for detailed view
        3. Adjust temperature threshold
        4. Upload EPW files
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.caption(f"""
    <div style="color: #7f8c8d; font-size: 0.8em; margin-top: 20px">
        Version: 1.1.0 | {datetime.now().strftime('%Y-%m-%d')}<br>
        Developed by Polla Sktani
    </div>
    """, unsafe_allow_html=True)
