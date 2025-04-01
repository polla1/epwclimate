# sidebar.py
import streamlit as st
from PIL import Image

def display_sidebar():
    """Display sidebar with enhanced UI/UX for file uploads and options."""
    st.sidebar.header("Climate Data Upload & Settings")

    # Optionally add an image (like a logo)
    image = Image.open('your_image_path/logo.png')
    st.sidebar.image(image, use_column_width=True)

    st.sidebar.markdown("### Upload Your Custom Climate Files")
    uploaded_files = st.sidebar.file_uploader(
        "Choose climate data files (EPW format)", type="csv", accept_multiple_files=True
    )

    st.sidebar.markdown("### Climate Scenarios")
    # Using a multi-select dropdown to choose scenarios
    scenarios = ['2023 Baseline', '2050 Projection', '2080 Projection']
    selected_scenarios = st.sidebar.multiselect(
        "Select the climate scenarios to display", options=scenarios, default=scenarios
    )

    # Adding a little help text
    st.sidebar.markdown("""
        **Note**: Choose which scenarios you want to visualize in the main chart.
        Use the file uploader to add your own climate data for comparison.
    """)

    return uploaded_files, selected_scenarios

