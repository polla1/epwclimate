import streamlit as st

def display_sidebar():
    """Modern sidebar with clean design"""
    
    # Custom styling
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background: #f8f9fa;
            padding: 25px !important;
            border-right: 1px solid #e0e0e0;
        }
        .sidebar-title {
            color: #2c3e50;
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid #4B32C3;
        }
        .guide-item {
            padding: 8px 0;
            font-size: 0.95em;
            color: #4a4a4a;
        }
        .contact-section {
            margin-top: 25px;
            padding: 15px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        .footer {
            margin-top: 25px;
            font-size: 0.75em;
            color: #7f8c8d;
            text-align: center;
            padding-top: 15px;
            border-top: 1px solid #eee;
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
        • Compare climate projections<br>
        <small>2023 Baseline vs 2050/2080 Scenarios</small>
    </div>
    <div class="guide-item">
        • Analyze monthly patterns<br>
        <small>Use month selector dropdown</small>
    </div>
    <div class="guide-item">
        • Calculate extreme heat<br>
        <small>Adjust temperature threshold slider</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Contact Information
    st.sidebar.markdown("---")
    with st.sidebar.container():
        st.markdown("#### 📮 Contact")
        st.markdown("""
        **Polla D. I. Sktani**  
        *MSc Sustainable Architecture*  
        [polla.sktani@gmail.com](mailto:polla.sktani@gmail.com)  
        [GitHub/polla1](https://github.com/polla1)
        """)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        '<div class="footer">Polla Sktani ©2025</div>', 
        unsafe_allow_html=True
    )
