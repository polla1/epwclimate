import streamlit as st

def display_sidebar():
    """Clean sidebar with proper spacing"""
    
    # Custom styling
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background: #f8f9fa;
            padding: 25px !important;
        }
        .sidebar-title {
            color: #2c3e50;
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 25px;
            padding-bottom: 10px;
            border-bottom: 2px solid #4B32C3;
        }
        .guide-item {
            padding: 8px 0;
            color: #4a4a4a;
            font-size: 0.95em;
        }
        .contact-section {
            margin: 25px 0;
            padding-top: 15px;
        }
        .footer {
            margin-top: 25px;
            font-size: 0.75em;
            color: #7f8c8d;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)

    # Main Title
    st.sidebar.markdown(
        '<div class="sidebar-title">📈 EPW Climate Toolkit</div>', 
        unsafe_allow_html=True
    )
    
    # User Guide
    st.sidebar.markdown("#### 🧭 Quick Guide")
    st.sidebar.markdown("""
    <div class="guide-item">
        • Compare 2023/2050/2080 projections
    </div>
    <div class="guide-item">
        • Analyze monthly patterns
    </div>
    <div class="guide-item">
        • Calculate extreme heat hours
    </div>
    """, unsafe_allow_html=True)
    
    # Contact Information
    st.sidebar.markdown("---")
    with st.sidebar.container():
        st.markdown("#### 📮 Contact")
        st.markdown("""
        **Polla D. I. Sktani**  
        MSc Sustainable Architecture  
        [polla.sktani@gmail.com](mailto:polla.sktani@gmail.com)  
        [GitHub/polla1](https://github.com/polla1)
        """)
    
    # Single footer with top border
    st.sidebar.markdown(
        '<div class="footer">Polla Sktani ©2025</div>', 
        unsafe_allow_html=True
    )
