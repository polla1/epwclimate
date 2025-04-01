import streamlit as st

def display_sidebar():
    with st.sidebar:
        st.title("⚙️ Settings")
        
        # Section: Data Upload
        with st.expander("📂 Upload Custom Data", expanded=True):
            st.info("Upload your own EPW files to compare custom climate data.")
            uploaded = st.file_uploader(
                "Choose EPW files",
                type="epw",
                accept_multiple_files=True,
                help="Upload EnergyPlus Weather (.epw) files."
            )
        
        # Section: Visualization Options
        with st.expander("📊 Chart Settings"):
            st.write("Customize how the data is displayed.")
            show_grid = st.checkbox("Show Gridlines", value=True)
            smooth_lines = st.checkbox("Smooth Temperature Curves")
        
        # Section: About the App
        with st.expander("ℹ️ About"):
            st.markdown(
                """
                **Climate Data Visualization**  
                This tool helps analyze climate projections for Erbil.
                - 📅 Compare different years
                - 🌡️ See temperature trends
                - 📂 Upload your own EPW files  
                """
            )
    
    return uploaded, show_grid, smooth_lines
