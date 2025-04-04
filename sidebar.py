import streamlit as st

def display_sidebar():
    """Clean sidebar with clickable GitHub link"""
    
    # Custom styling
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            padding: 20px !important;
        }
        .sidebar-title {
            color: #2c3e50;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .footer {
            margin-top: 20px;
            font-size: 0.8em;
            color: #666;
            text-align: center;
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
    **Polla D. I. Sktani**  
    MSc Sustainable Architecture  
    polla.sktani@gmail.com  
    GitHub: [polla1](https://github.com/polla1)
    """)
    
    # Single footer
    st.sidebar.markdown("---")
    st.sidebar.markdown('<div class="footer">Polla Sktani ©2025</div>', unsafe_allow_html=True)
