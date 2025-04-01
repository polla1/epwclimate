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

# Static CSS for better performance
SLIDER_CSS = """
<style>
    div[data-baseweb="slider"] > div { 
        background: linear-gradient(90deg, #90EE90 0%, #FFA500 50%, #FF4500 100%);
        height: 8px;
        border-radius: 4px;
    }
    .severity-box {
        text-align: center; 
        padding: 8px; 
        border-radius: 5px; 
        width: 32%;
        margin: 5px 0;
        transition: background-color 0.2s;
    }
</style>
"""

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
    st.markdown(SLIDER_CSS, unsafe_allow_html=True)
    st.title("🌡️ Erbil Climate Projections")
    
    # Initialize session state
    if 'threshold' not in st.session_state:
        st.session_state.threshold = 40
    
    # Load data
    erbil_data = load_erbil_data()
    uploaded_files = display_sidebar()
    
    # [Keep Chart 1 and Chart 2 code exactly as in your working version]
    
    # ===== Chart 3: Extreme Heat Analysis =====
    st.header("3. Extreme Heat Analysis")
    
    # Threshold controls with debouncing
    new_threshold = st.slider(
        "Select temperature threshold (°C)",
        min_value=30,
        max_value=60,
        value=st.session_state.threshold,
        step=1,
        help="Analyze hours above this temperature level",
        key="temp_threshold"
    )
    
    # Update threshold only when changed
    if new_threshold != st.session_state.threshold:
        st.session_state.threshold = new_threshold
        st.experimental_rerun()
    
    # Severity indicators
    cols = st.columns(3)
    with cols[0]:
        st.markdown(f"""
        <div class="severity-box" style="background: {'#90EE90' if st.session_state.threshold <35 else '#f0f0f0'}">
            🌱 Mild<br><small>(<35°C)</small>
        </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"""
        <div class="severity-box" style="background: {'#FFA500' if 35<=st.session_state.threshold<45 else '#f0f0f0'}">
            🔥 Hot<br><small>(35-44°C)</small>
        </div>
        """, unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f"""
        <div class="severity-box" style="background: {'#FF4500' if st.session_state.threshold>=45 else '#f0f0f0'}">
            ☠️ Extreme<br><small>(≥45°C)</small>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")

    # Cached calculations
    @st.cache_data
    def get_hours_data(_threshold):
        return {
            '2023 Baseline': count_hours_above_threshold(load_baseline(), _threshold),
            '2050 Projection': count_hours_above_threshold(load_2050(), _threshold),
            '2080 Projection': count_hours_above_threshold(load_2080(), _threshold)
        }
    
    hours_data = get_hours_data(st.session_state.threshold)
    
    # Create chart
    heat_labels = {30: "🌡️ Warm", 40: "🔥 Hot", 50: "☠️ Extreme", 60: "💀 Danger"}
    closest_label = min(heat_labels.keys(), key=lambda x: abs(x - st.session_state.threshold))
    
    chart = alt.Chart(pd.DataFrame({
        'Scenario': list(hours_data.keys()),
        'Hours': list(hours_data.values())
    }).mark_bar(
        cornerRadius=8,
        stroke='#333333',
        strokeWidth=0.5
    ).encode(
        x=alt.X('Scenario:N', title=''),
        y=alt.Y('Hours:Q', title='Hours Above Threshold'),
        color=alt.Color('Scenario:N').scale(
            domain=list(ERBIL_COLORS.keys()),
            range=list(ERBIL_COLORS.values())
        ),
        tooltip=['Scenario', alt.Tooltip('Hours:Q', format=',')]
    ).properties(
        height=400,
        title=f"{heat_labels[closest_label]} Heat Hours: Above {st.session_state.threshold}°C"
    )
    
    st.altair_chart(chart, use_container_width=True)
    
    # [Keep footer code exactly as in your working version]

if __name__ == "__main__":
    main()
