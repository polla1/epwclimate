import streamlit as st
import pandas as pd
import altair as alt
from database import load_baseline, load_2050, load_2080, read_epw, count_hours_above_threshold
from sidebar import display_sidebar
from contact import display_contact

ERBIL_COLORS = {
    '2023 Baseline': '#00FF00',
    '2050 Projection': '#0000FF',
    '2080 Projection': '#FF0000'
}

def create_chart(data, colors, title, x_axis='DateTime:T', x_format='%B'):
    df_melted = data.reset_index().melt(
        id_vars=['DateTime'],
        var_name='Scenario',
        value_name='Temperature'
    )
    return alt.Chart(df_melted).mark_line(
        opacity=0.7,
        strokeWidth=2
    ).encode(
        x=alt.X(x_axis, title='Month', axis=alt.Axis(format=x_format)),
        y=alt.Y('Temperature:Q', title='Temperature (°C)'),
        color=alt.Color('Scenario:N').scale(
            domain=list(colors.keys()),
            range=list(colors.values())
        ),
        tooltip=['Scenario', 'DateTime', alt.Tooltip('Temperature:Q', format='.1f')]
    ).properties(
        height=400,
        title=title
    )

@st.cache_data
def load_erbil_data():
    return pd.concat([
        load_baseline().rename(columns={'Temperature': '2023 Baseline'}),
        load_2050().rename(columns={'Temperature': '2050 Projection'}),
        load_2080().rename(columns={'Temperature': '2080 Projection'})
    ], axis=1)

def show_erbil_analysis(erbil_data):
    """Erbil Projections Analysis"""
    st.header("Erbil Climate Projections")
    
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

        hours_data = {
            '2023 Baseline': count_hours_above_threshold(load_baseline(), threshold),
            '2050 Projection': count_hours_above_threshold(load_2050(), threshold),
            '2080 Projection': count_hours_above_threshold(load_2080(), threshold)
        }
        
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

def show_epw_analysis():
    """Custom EPW Analysis"""
    st.header("Custom EPW Analysis")
    
    with st.container():
        st.subheader("📤 Upload EPW Files")
        uploaded_files = st.file_uploader(
            "Select EPW weather files",
            type="epw",
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        
        if uploaded_files:
            st.success(f"{len(uploaded_files)} file(s) selected:")
            for file in uploaded_files:
                st.write(f"- {file.name}")
            
            if st.button("Clear Files", key="epw_clear"):
                st.experimental_rerun()
    
    if uploaded_files:
        try:
            epw_dfs = []
            for idx, file in enumerate(uploaded_files):
                epw_data = read_epw(file)
                epw_data = epw_data.rename(columns={'Temperature': f'Custom {idx+1}'})
                epw_dfs.append(epw_data)
            
            combined_epw = pd.concat(epw_dfs, axis=1)
            
            st.altair_chart(
                create_chart(
                    combined_epw,
                    {col: '#8A2BE2' for col in combined_epw.columns},
                    "EPW Temperature Analysis",
                    x_axis='DateTime:T',
                    x_format='%B'
                ), use_container_width=True
            )
            
            if st.checkbox("Show raw data preview", key="epw_preview"):
                st.dataframe(combined_epw.head())

        except Exception as e:
            st.error(f"EPW Processing Error: {str(e)}")
            st.markdown("""
            **Required Format:**
            - Valid EPW file structure
            - Contains temperature data column
            - Proper datetime formatting
            """)
    else:
        st.info("Please upload EPW files above to begin analysis")

def main():
    st.set_page_config(page_title="Climate Analysis", layout="wide")
    
    # Custom tab styling (updated)
    st.markdown("""
    <style>
        /* Target only the tab headers */
        button[data-testid="baseButton-header"] {
            font-size: 18px !important;
            font-weight: 500 !important;
            padding: 12px 24px !important;
            margin: 0 4px !important;
            border-radius: 8px 8px 0 0 !important;
            transition: all 0.3s ease !important;
            border-bottom: 3px solid transparent !important;
        }
        
        /* Active tab styling */
        button[data-testid="baseButton-header"][aria-selected="true"] {
            background: #f0f2f6 !important;
            color: #2c3e50 !important;
            border-bottom: 3px solid #4a90e2 !important;
            transform: translateY(-1px);
        }
        
        /* Inactive tab styling */
        button[data-testid="baseButton-header"][aria-selected="false"] {
            background: #dfe6e9 !important;
            color: #7f8c8d !important;
            opacity: 0.9;
        }
        
        /* Hover effects */
        button[data-testid="baseButton-header"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Rest of your existing main() code remains unchanged...
    
    st.title("🌡️ Climate Analysis Dashboard")
    
    erbil_data = load_erbil_data()
    
    tab1, tab2 = st.tabs([
        "🌍 Erbil Projections", 
        "📤 Custom EPW Analysis"
    ])
    
    with tab1:
        show_erbil_analysis(erbil_data)
    
    with tab2:
        show_epw_analysis()
    
    display_contact()
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<center> Polla Sktani ©2025 </center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
