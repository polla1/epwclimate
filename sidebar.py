import streamlit as st

def display_sidebar():
    # Sidebar header
    st.sidebar.header("📊 Climate Data Analysis")
    st.sidebar.subheader("Upload EPW Files")
    st.sidebar.write("Upload (EPW format) files to visualize temperature projections for other cities.")
    
    # File uploader with customizations
    uploaded_files = st.sidebar.file_uploader(
        "Choose EPW files to upload",
        type="epw",
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    # Show uploaded file names in a neat list
    if uploaded_files:
        st.sidebar.write("### Files Uploaded:")
        for file in uploaded_files:
            st.sidebar.write(f"- {file.name}")
    
    # Reset button to clear the uploaded files
    if uploaded_files:
        if st.sidebar.button("Reset Files"):
            uploaded_files = None
            st.sidebar.write("### Files Reset")
            st.experimental_rerun()

    # Information panel or instructions for users
    st.sidebar.markdown("""
    ## 🌍 About
    The climate analysis tool allows you to visualize and analyze temperature projections (2023, 2050, and 2080). 
    Upload your own EPW files to compare projections. 

    ## 📅 Monthly Temperature Analysis
    Select a month from the dropdown to view temperature trends.
    """)
    
    return uploaded_files
