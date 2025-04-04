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
    # In display_sidebar() function:
st.sidebar.markdown("### 🧭 Quick Guide")
st.sidebar.markdown("""
<style>
    .guide-card {
        padding: 12px;
        margin: 10px 0;
        border-radius: 8px;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    .guide-card:hover {
        transform: translateX(5px);
    }
    .guide-icon {
        font-size: 20px;
        margin-right: 10px;
        vertical-align: middle;
    }
    .guide-bullet {
        color: #4B32C3;
        font-weight: bold;
        margin-right: 8px;
    }
</style>

<div class="guide-card">
    <span class="guide-icon">🌍</span>
    <span class="guide-bullet">•</span>
    Compare climate projections
    <div style="margin-left: 38px; font-size: 0.9em; color: #666">
    2023 Baseline vs 2050/2080 Scenarios
    </div>
</div>

<div class="guide-card">
    <span class="guide-icon">📅</span>
    <span class="guide-bullet">•</span>
    Analyze monthly patterns
    <div style="margin-left: 38px; font-size: 0.9em; color: #666">
    Detailed temperature trends by month
    </div>
</div>

<div class="guide-card">
    <span class="guide-icon">🌡️</span>
    <span class="guide-bullet">•</span>
    Calculate extreme heat
    <div style="margin-left: 38px; font-size: 0.9em; color: #666">
    Hours above custom temperature thresholds
    </div>
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
