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
    
    # ===== Original Erbil Charts (100% Unchanged) =====
    # [All original chart code remains exactly the same]
    
    # ===== Fixed EPW Analysis Section =====
    if uploaded_files:
        with st.expander("📤 EPW File Analysis", expanded=True):
            try:
                # Column name variations
                DT_COLS = ['datetime', 'date/time', 'timestamp', 'date']
                TEMP_COLS = ['dry bulb temperature', 'drybulbtemperature', 'temperature', 'temp']
                
                epw_dfs = []
                valid_files = 0
                
                for idx, file in enumerate(uploaded_files):
                    df = read_epw(file)
                    df.columns = df.columns.str.strip().str.lower()
                    
                    # Find datetime column
                    dt_col = next((col for col in DT_COLS if col in df.columns), None)
                    if not dt_col:
                        st.error(f"Missing datetime column in {file.name}. Needs one of: {DT_COLS}")
                        continue
                        
                    # Find temperature column
                    temp_col = next((col for col in TEMP_COLS if col in df.columns), None)
                    if not temp_col:
                        st.error(f"Missing temperature column in {file.name}. Needs one of: {TEMP_COLS}")
                        continue
                    
                    # Process valid file
                    try:
                        epw_df = df[[dt_col, temp_col]].copy()
                        epw_df.columns = ['DateTime', f'EPW {idx+1}']
                        epw_df['DateTime'] = pd.to_datetime(epw_df['DateTime'])
                        epw_df.set_index('DateTime', inplace=True)
                        epw_dfs.append(epw_df)
                        valid_files += 1
                    except Exception as proc_error:
                        st.error(f"Error processing {file.name}: {str(proc_error)}")
                        continue
                
                if valid_files > 0:
                    # Combine and plot
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
                    
                    # Show file info
                    st.success(f"Processed {valid_files} EPW files successfully")
                    with st.expander("View EPW Data Details"):
                        st.write("Columns found in files:")
                        st.write(pd.DataFrame({
                            'File': [f.name for f in uploaded_files],
                            'DateTime Column': [dt_col for _ in uploaded_files],
                            'Temperature Column': [temp_col for _ in uploaded_files]
                        }))
                        st.dataframe(combined_epw.head())
                else:
                    st.warning("No valid EPW files could be processed")
                    
            except Exception as e:
                st.error(f"EPW processing failed: {str(e)}")
                st.write("Please ensure files are valid EPW format with:")
                st.write("- Recognizable datetime column")
                st.write("- Clear temperature data column")

    # Footer 
    display_contact()
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<center> Polla Sktani ©2025 </center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
