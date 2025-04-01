def display_sidebar():
    with st.sidebar:
        st.header("Custom Data Upload")
        uploaded = st.file_uploader(
            "Upload EPW files",
            type="epw",
            accept_multiple_files=True
        )
    return uploaded
