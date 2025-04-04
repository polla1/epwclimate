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

def create_chart(data, colors, title, x_format='%B'):
    try:
        df_melted = data.reset_index().melt(
            id_vars=['DateTime'],
            var_name='Scenario',
            value_name='Temperature'
        )
        return alt.Chart(df_melted).mark_line(opacity=0.7).encode(
            x=alt.X('DateTime:T', title='Month', axis=alt.Axis(format=x_format)),
            y=alt.Y('Temperature:Q', title='Temperature (°C)'),
            color=alt.Color('Scenario:N').scale(domain=list(colors.keys()), range=list(colors.values())),
            tooltip=['Scenario', 'DateTime', alt.Tooltip('Temperature:Q', format='.1f')]
        ).properties(height=400, title=title)
    except Exception as e:
        st.error(f"Chart error: {str(e)}")
        return None

@st.cache_data
def load_erbil_data():
    return pd.concat([
        load_baseline().rename(columns={'Temperature': '2023 Baseline'}),
        load_2050().rename(columns={'Temperature': '2050 Projection'}),
        load_2080().rename(columns={'Temperature': '2080 Projection'})
    ], axis=1)

def process_epw(uploaded_files):
    if not uploaded_files:
        return None
    
    try:
        epw_dfs = []
        for i, file in enumerate(uploaded_files):
            df = read_epw(file)
            if 'Dry Bulb Temperature' not in df.columns:
                raise ValueError("EPW file missing 'Dry Bulb Temperature' column")
                
            df = df.rename(columns={'Dry Bulb Temperature': f'EPW {i+1}'})
            epw_dfs.append(df[['DateTime', f'EPW {i+1}']])
        
        return pd.concat(epw_dfs, axis=1).ffill()
    except Exception as e:
        st.error(f"EPW Error: {str(e)}")
        return None

def main():
    st.set_page_config(page_title="Climate Analysis", layout="wide")
    st.title("🌡️ Climate Analysis Tool")
    
    # Load core data
    erbil_data = load_erbil_data()
    uploaded_files = display_sidebar()
    
    # ===== Erbil Analysis =====
    st.header("Erbil Climate Projections")
    
    # Chart 1: Scenario Comparison
    with st.container():
        st.subheader("🌍 Scenario Comparison")
        selected = [scenario for scenario in ERBIL_COLORS 
                   if st.checkbox(scenario, True, key=f"erbil_{scenario}")]
        
        if selected:
            chart = create_chart(erbil_data[selected], ERBIL_COLORS, "Temperature Projections")
            if chart: st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("Select at least one scenario")

    # Chart 2: Monthly Analysis
    with st.container():
        st.subheader("📅 Monthly Patterns")
        month = st.selectbox("Select Month", range(1,13), 
                           format_func=lambda x: pd.Timestamp(2023, x, 1).strftime('%B'))
        monthly_data = erbil_data[erbil_data.index.month == month]
        if not monthly_data.empty:
            chart = create_chart(monthly_data, ERBIL_COLORS, 
                               f"Hourly Temperatures in {pd.Timestamp(2023, month, 1).strftime('%B')}",
                               x_format='%d')
            if chart: st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("No data for selected month")

    # Chart 3: Heat Analysis
    with st.container():
        st.subheader("🔥 Extreme Heat")
        threshold = st.slider("Temperature Threshold (°C)", 30, 58, 40,
                            help="Analyze hours above this temperature")
        
        # Calculate hours
        hours_data = {
            scenario: count_hours_above_threshold(df, threshold)
            for scenario, df in zip(
                ['2023 Baseline', '2050 Projection', '2080 Projection'],
                [load_baseline(), load_2050(), load_2080()]
            )
        }
        
        # Display chart
        chart = alt.Chart(pd.DataFrame({
            'Scenario': list(hours_data.keys()),
            'Hours': list(hours_data.values())
        })).mark_bar().encode(
            x=alt.X('Scenario:N', title=''),
            y=alt.Y('Hours:Q', title='Hours Above Threshold'),
            color=alt.Color('Scenario:N').scale(domain=list(ERBIL_COLORS.keys()), 
            range=list(ERBIL_COLORS.values()))
        ).properties(height=400, title=f"Hours Above {threshold}°C")
        
        st.altair_chart(chart, use_container_width=True)

    # ===== EPW Analysis =====
    if uploaded_files:
        st.header("📤 Custom EPW Analysis")
        epw_data = process_epw(uploaded_files)
        
        if epw_data is not None:
            st.subheader("Temperature Analysis")
            epw_colors = {col: '#8A2BE2' for col in epw_data.columns if col != 'DateTime'}
            chart = create_chart(epw_data, epw_colors, "EPW Temperature Data")
            if chart: st.altair_chart(chart, use_container_width=True)
            
            st.subheader("File Details")
            st.write(f"Uploaded files: {len(uploaded_files)}")
            st.dataframe(epw_data.describe())

    # Footer
    display_contact()
    st.markdown("---")
    st.caption("© 2024 Climate Analysis Tool")

if __name__ == "__main__":
    main()
