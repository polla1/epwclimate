import streamlit as st

def display_sidebar():
    st.sidebar.header("📊 Climate Data Analysis")
    
    # File uploader
    uploaded_files = st.sidebar.file_uploader(
        "Upload EPW files to compare projections",
        type="epw",
        accept_multiple_files=True
    )

    # Show uploaded file names in a compact format
    if uploaded_files:
        st.sidebar.markdown("**Files Uploaded:**")
        for file in uploaded_files:
            st.sidebar.caption(f"📄 {file.name}")

    # Reset button
    if uploaded_files and st.sidebar.button("Reset Files"):
        uploaded_files = None
        st.sidebar.experimental_rerun()

    # Separator
    st.sidebar.markdown("---")

    # Compact information panel
    st.sidebar.caption("🌍 **Compare climate projections (2023, 2050, 2080).**")
    st.sidebar.caption("📅 **Use the dropdown to analyze monthly trends.**")
    
    return uploaded_files
