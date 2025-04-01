import streamlit as st

def display_sidebar():
    """Display an improved sidebar with sections, a multi-select, and help text."""
    with st.sidebar:
        st.header("📂 Custom Data Upload")
        uploaded_files = st.file_uploader(
            "Upload EPW files",
            type="epw",
            accept_multiple_files=True
        )

        st.markdown("---")  # Adds a separator for better UI

        st.header("🌍 Climate Scenarios")
        scenarios = ['2023 Baseline', '2050 Projection', '2080 Projection']
        selected_scenarios = st.multiselect(
            "Select climate scenarios to display:",
            options=scenarios,
            default=scenarios  # Pre-select all
        )

        st.markdown("---")  

        st.info(
            "🔹 Upload your own EPW files to compare with Erbil projections. "
            "You can also select different climate scenarios to visualize."
        )

    return uploaded_files, selected_scenarios
