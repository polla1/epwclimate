def main():
    st.set_page_config(page_title="Climate Analysis", layout="wide")
    st.title("🌡️ Erbil Climate Projections")
    
    # Load data
    erbil_data = load_erbil_data()
    uploaded_files = display_sidebar()
    
    # Create tabs
    tab1, tab2 = st.tabs(["Erbil Climate Analysis", "Custom EPW Analysis"])
    
    with tab1:
        # ===== Original 3 Charts =====
        # Chart 1: Scenarios
        st.markdown("### 🌍 Climate Scenario Comparison")
        selected_erbil = []
        cols = st.columns(3)
        for i, scenario in enumerate(ERBIL_COLORS):
            with cols[i]:
                if st.checkbox(scenario, value=True, key=f"erbil_{i}"):
                    selected_erbil.append(scenario)
        
        if selected_erbil:
            st.altair_chart(
                create_chart(
                    erbil_data[selected_erbil],
                    {k: v for k, v in ERBIL_COLORS.items() if k in selected_erbil},
                    "Temperature Projections Over Time"
                ), use_container_width=True)
        else:
            st.warning("Please select at least one scenario")

        # Chart 2: Monthly Analysis
        st.markdown("### 📅 Monthly Temperature Patterns")
        month = st.selectbox(
            "Select Month", 
            range(1, 13), 
            format_func=lambda x: pd.Timestamp(2023, x, 1).strftime('%B'),
            key="month_select"
        )
        monthly_data = erbil_data[erbil_data.index.month == month]
        if not monthly_data.empty:
            st.altair_chart(
                create_chart(
                    monthly_data,
                    ERBIL_COLORS,
                    f"Hourly Temperatures in {pd.Timestamp(2023, month, 1).strftime('%B')}",
                    x_axis='DateTime:T',
                    x_format='%d'
                ), use_container_width=True)
        else:
            st.warning("No data for selected month")

        # Chart 3: Extreme Heat Analysis
        st.markdown("### 🔥 Extreme Heat Analysis")
        # ... [Keep all the existing Extreme Heat Analysis code unchanged] ...

    with tab2:
        # ===== Custom EPW Analysis =====
        st.markdown("## 📤 Custom EPW File Analysis")
        if uploaded_files:
            try:
                custom_data = pd.concat([read_epw(file) for file in uploaded_files], axis=1)
                custom_colors = {col: '#8A2BE2' for col in custom_data.columns}  # Purple color
                
                st.altair_chart(
                    create_chart(
                        custom_data,
                        custom_colors,
                        "Custom EPW Temperature Analysis",
                        x_axis='DateTime:T',
                        x_format='%B'
                    ), use_container_width=True
                )
                
                # Optional: Add EPW-specific analysis
                st.markdown("### 📊 EPW File Statistics")
                st.write(f"Number of files uploaded: {len(uploaded_files)}")
                st.write("Custom data summary:")
                st.dataframe(custom_data.describe())
                
            except Exception as e:
                st.error(f"Error processing EPW files: {str(e)}")
        else:
            st.info("Please upload EPW files using the sidebar controls")
    
    # Footer (outside tabs)
    display_contact()
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<center> Polla Sktani ©2025 </center>", unsafe_allow_html=True)
