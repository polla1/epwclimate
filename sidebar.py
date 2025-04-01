import streamlit as st

def display_sidebar():
    st.sidebar.header("📊 Climate Data Analysis")
    st.sidebar.subheader("Upload EPW Files")

    uploaded_files = st.sidebar.file_uploader(
        "Upload custom EPW files",
        type="epw",
        accept_multiple_files=True
    )

    if uploaded_files:
        st.sidebar.markdown("**📂 Uploaded Files:**")
        for file in uploaded_files:
            st.sidebar.caption(f"✔ {file.name}")

        if st.sidebar.button("Reset Files"):
            st.sidebar.experimental_rerun()

    st.sidebar.markdown("---")
    st.sidebar.caption("🌍 Compare climate projections (2023, 2050, 2080).")
    st.sidebar.caption("📅 Use the dropdown to analyze monthly trends.")

    return uploaded_files
