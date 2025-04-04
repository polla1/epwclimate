import streamlit as st

def display_sidebar():
    """Simplified sidebar with minimal content"""
    
    # Custom styling
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            padding: 20px !important;
        }
        .sidebar-title {
            color: #2c3e50;
            font-size: 20px !important;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .contact-info {
            margin-top: 30px;
            font-size: 0.9em;
            color: #666;
        }
    </style>
    """, unsafe_allow_html=True)

    # Main Title
    st.sidebar.markdown('<div class="sidebar-title">EPW Weather File Toolkit</div>', unsafe_allow_html=True)
    
    # User Guide
    st.sidebar.markdown("### ℹ️ User Guide")
    st.sidebar.markdown("""
    - 🌍 Compare climate projections (2023, 2050, 2080)
    - 📅 Use dropdown to analyze monthly trends
    - 🌡️ Move selector for hours above threshold
    """)
    
    # Contact Information
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Contact Information")
    st.sidebar.markdown("""

    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown('<div class="contact-info">Polla Sktani ©2025</div>', unsafe_allow_html=True)
