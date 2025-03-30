# app.py (modified section)
def main():
    st.title("Erbil City Temperature Analysis")
    
    # Load data with caching
    data = load_all_data()
    combined = pd.concat([
        data['baseline'].rename(columns={'Temperature': 'Baseline 2023'}),
        data['2050'].rename(columns={'Temperature': 'Future 2050'}),
        data['2080'].rename(columns={'Temperature': 'Future 2080'})
    ], axis=1)

    # Process uploaded files
    uploaded_files = display_sidebar()
    for file in uploaded_files:
        temp_df = read_epw(file)
        combined[file.name] = temp_df['Temperature']

    # Yearly visualization with toggle controls
    st.header("Yearly Temperature Comparison")
    
    # Create toggle buttons in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        show_baseline = st.checkbox("Baseline 2023", value=True)
    with col2:
        show_2050 = st.checkbox("Future 2050", value=True)
    with col3:
        show_2080 = st.checkbox("Future 2080", value=True)

    # Filter data based on selections
    selected_columns = []
    if show_baseline:
        selected_columns.append('Baseline 2023')
    if show_2050:
        selected_columns.append('Future 2050')
    if show_2080:
        selected_columns.append('Future 2080')
    
    # Add uploaded files toggles
    if uploaded_files:
        st.write("Uploaded Files:")
        file_toggles = {}
        for file in uploaded_files:
            file_toggles[file.name] = st.checkbox(file.name, value=True)
        
        selected_columns += [name for name, show in file_toggles.items() if show]

    # Plot filtered data
    if selected_columns:
        st.line_chart(combined[selected_columns])
    else:
        st.warning("Please select at least one scenario to display")

    # Keep existing monthly analysis section unchanged
    # ...
