def show_erbil_analysis():
    """Main page with original 3 charts"""
    erbil_data = load_erbil_data()
    
    # ===== Chart 1: Scenarios =====
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

    # ===== Chart 2: Monthly Analysis =====
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

    # ===== Chart 3: Extreme Heat Analysis =====
    st.markdown("### 🔥 Extreme Heat Analysis")
    
    # Threshold controls
    with st.container():
        st.markdown("#### 🌡️ Temperature Threshold Selector")
        
        st.markdown("""
        <style>
            div[data-baseweb="slider"] > div { 
                background: linear-gradient(90deg, #90EE90 0%, #FFA500 50%, #FF4500 100%);
                height: 8px;
                border-radius: 4px;
            }
        </style>
        """, unsafe_allow_html=True)
        
        threshold = st.slider(
            "Select temperature threshold (°C)",
            min_value=30,
            max_value=58,
            value=40,
            step=1,
            help="Analyze hours above this temperature level",
            key="temp_threshold"
        )
        
        severity_html = f"""
        <div style="display: flex; justify-content: space-between; margin: 10px 0;">
            <div style="text-align: center; background: {'#90EE90' if threshold <35 else '#f0f0f0'}; 
                        padding: 8px; border-radius: 5px; width: 32%;">
                🌱 Mild<br><small>(<35°C)</small>
            </div>
            <div style="text-align: center; background: {'#FFA500' if 35<=threshold<45 else '#f0f0f0'}; 
                        padding: 8px; border-radius: 5px; width: 32%;">
                🔥 Hot<br><small>(35-44°C)</small>
            </div>
            <div style="text-align: center; background: {'#FF4500' if threshold>=45 else '#f0f0f0'}; 
                        padding: 8px; border-radius: 5px; width: 32%;">
                ☠️ Extreme<br><small>(≥45°C)</small>
            </div>
        </div>
        """
        st.markdown(severity_html, unsafe_allow_html=True)
        st.markdown("---")

    # Calculate and display hours
    hours_data = {
        '2023 Baseline': count_hours_above_threshold(load_baseline(), threshold),
        '2050 Projection': count_hours_above_threshold(load_2050(), threshold),
        '2080 Projection': count_hours_above_threshold(load_2080(), threshold)
    }
    
    # Create chart
    chart = alt.Chart(
        pd.DataFrame({
            'Scenario': list(hours_data.keys()),
            'Hours': list(hours_data.values())
        })
    ).mark_bar().encode(
        x=alt.X('Scenario:N', title='', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Hours:Q', title='Hours Above Threshold'),
        color=alt.Color('Scenario:N').scale(
            domain=list(ERBIL_COLORS.keys()),
            range=list(ERBIL_COLORS.values())
        ),
        tooltip=['Scenario', alt.Tooltip('Hours:Q', format=',')]
    ).properties(
        height=400,
        title=f"Heat Hours Above {threshold}°C"
    )
    
    st.altair_chart(chart, use_container_width=True)
