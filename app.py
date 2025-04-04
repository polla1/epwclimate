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
    
    # Load data
    erbil_data = load_erbil_data()
    uploaded_files = display_sidebar()
    
    # ===== Original 3 Charts =====
    # [Keep all your original chart code here - unchanged]
    
    # ===== Fixed EPW Visualization =====
    if uploaded_files:
        with st.expander("📤 Uploaded EPW File Analysis", expanded=True):
            try:
                # Process EPW files with correct column names
                epw_dfs = []
                for i, file in enumerate(uploaded_files):
                    df = read_epw(file)
                    # Rename temperature column explicitly
                    df = df.rename(columns={'Dry Bulb Temperature': 'Temperature'})
                    df = df[['DateTime', 'Temperature']]
                    df = df.rename(columns={'Temperature': f'Custom EPW {i+1}'})
                    epw_dfs.append(df)

                custom_data = pd.concat(epw_dfs, axis=1)
                custom_colors = {col: '#8A2BE2' for col in custom_data.columns if col != 'DateTime'}

                # Create EPW chart using existing function
                st.altair_chart(
                    create_chart(
                        custom_data.filter(regex='^(?!DateTime)'),
                        custom_colors,
                        "Custom EPW Temperature Analysis",
                        x_axis='DateTime:T',
                        x_format='%B'
                    ), use_container_width=True
                )

                # Show file info
                st.write(f"Successfully processed {len(uploaded_files)} EPW files")
                with st.expander("View raw EPW data"):
                    st.dataframe(custom_data.head())

            except Exception as e:
                st.error(f"EPW processing failed: {str(e)}")
                st.write("Please ensure uploaded files are valid EPW format with 'Dry Bulb Temperature' column")

    # Footer 
    display_contact()
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<center> Polla Sktani ©2025 </center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
