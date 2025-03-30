import streamlit as st

def display_contact():
    with st.sidebar:
        st.header("Contact Information")
        st.markdown("""
        **Polla D. I. Sktani**  
        MSc Sustainable Architecture  
        [polla.sktani@gmail.com](mailto:polla.sktani@gmail.com)  
        [GitHub: polla1](https://github.com/polla1)
        
        ---
        
        *Polla Sktani ©2025*
        """, unsafe_allow_html=True)
