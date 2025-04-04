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

def main():
    st.set_page_config(page_title="Climate Analysis", layout="wide")
    st.title("🌡️ Erbil Climate Projections")
    
    # Load core data
    erbil_data = load_erbil_data()
    
    try:
        uploaded_files = display_sidebar()
    except Exception as e:
        st.error(f"Sidebar error: {str(e)}")
        uploaded_files = None
    
    # ===== Chart 1: Climate Scenario Comparison =====
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

    # ===== Chart 2: Monthly Temperature Patterns =====
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

    # ===== EPW File Analysis =====
    if uploaded_files:
        with st.expander("📤 EPW File Analysis", expanded=True):
            try:
                TEMP_COLUMNS = ['dry bulb temperature', 'drybulbtemperature', 'temperature']
                epw_dfs = []
                valid_files = 0
                
                for idx, file in enumerate(uploaded_files):
                    df = read_epw(file)
                    df.columns = df.columns.str.lower()
                    
                    # Find temperature column
                    temp_col = next((col for col in TEMP_COLUMNS if col in df.columns), None)
                    
                    if temp_col:
                        epw_df = df[['datetime', temp_col]].copy()
                        epw_df.columns = ['DateTime', f'EPW {idx+1}']
                        epw_dfs.append(epw_df)
                        valid_files += 1
                    else:
                        st.error(f"EPW file {file.name} missing temperature column. Needs one of: {TEMP_COLUMNS}")
                        
                if valid_files > 0:
                    combined_epw = pd.concat(epw_dfs, axis=1)
                    st.altair_chart(
                        create_chart(
                            combined_epw.filter(regex='EPW'),
                            {'EPW': '#8A2BE2'},
                            "EPW Temperature Analysis",
                            x_axis='DateTime:T',
                            x_format='%B'
                        ), use_container_width=True
                    )
                    st.success(f"Processed {valid_files} EPW file(s)")
                else:
                    st.warning("No valid EPW files found")
                    
            except Exception as e:
                st.error(f"EPW processing error: {str(e)}")

    # Footer
    display_contact()
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<center> Polla Sktani ©2025 </center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
