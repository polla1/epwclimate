import streamlit as st

def display_sidebar():
    """Modern sidebar design with improved visuals"""
    
    # Custom styling
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background: #f8f9fa;
            padding: 25px !important;
        }
        .sidebar-title {
            color: #2c3e50;
            font-size: 24px;
            font-weight: 800;
            margin-bottom: 25px;
            padding: 10px;
            background: linear-gradient(45deg, #4B32C3, #4472C4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
        }
        .guide-item {
            padding: 8px 0;
            font-size: 0.95em;
        }
        .contact-box {
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin: 15px 0;
        }
        .github-link {
            color: #2c3e50 !important;
            font-weight: 500;
            text-decoration: none;
            background: #f0f2f6;
            padding: 5px 10px;
            border-radius: 5px;
            display: inline-block;
            margin-top: 8px;
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
        '<div class="sidebar-title">📊 EPW Weather File Toolkit</div>', 
        unsafe_allow_html=True
    )
    
    # User Guide
    with st.sidebar.expander("📘 User Guide", expanded=True):
        st.markdown("""
        <div class="guide-item">
            🌍 Compare climate projections<br>
            <small>(2023 Baseline, 2050 & 2080 Scenarios)</small>
        </div>
        <div class="guide-item">
            📅 Analyze monthly trends<br>
            <small>(Select month from dropdown)</small>
        </div>
        <div class="guide-item">
            🌡️ Find extreme heat hours<br>
            <small>(Adjust temperature threshold)</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Contact Information
    st.sidebar.markdown("---")
    with st.sidebar.container():
        st.markdown('<div class="contact-box">', unsafe_allow_html=True)
        st.markdown("#### 📬 Contact Information")
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("""
            <style>
                .contact-icon {font-size: 20px; margin-right: 10px;}
            </style>
            <div class="contact-icon">👤</div>
            <div class="contact-icon">🎓</div>
            <div class="contact-icon">📧</div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            Polla D. I. Sktani  
            MSc Sustainable Architecture  
            [polla.sktani@gmail.com](mailto:polla.sktani@gmail.com)  
            """)
        st.markdown("""
        <a href="https://github.com/polla1" class="github-link">
            <img src="https://img.icons8.com/ios-glyphs/20/2c3e50/github.png" alt="GitHub"/>
            polla1
        </a>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.sidebar.markdown(
        '<div class="footer">Version 1.2.0<br>Polla Sktani ©2025</div>', 
        unsafe_allow_html=True
    )
