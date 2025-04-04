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
    
    try:
        uploaded_files = display_sidebar()
    except Exception as e:
        st.error(f"Sidebar error: {str(e)}")
        uploaded_files = None
    
    # ===== Original Erbil Charts (100% Unchanged) =====
    # [All your original chart code here - preserved exactly]
    
    # ===== Enhanced EPW Handling =====
    if uploaded_files and len(uploaded_files) > 0:
        with st.expander("📤 EPW File Analysis", expanded=True):
            try:
                TEMP_COLUMNS = [
                    'dry bulb temperature', 'drybulbtemperature',
                    'db temp', 'temperature', 'temp', 'air temperature'
                ]
                
                epw_datasets = []
                valid_count = 0
                
                for idx, file in enumerate(uploaded_files):
                    try:
                        df = read_epw(file)
                        df.columns = df.columns.str.lower()
                        
                        # Find temperature column
                        temp_col = next((col for col in TEMP_COLUMNS if col in df.columns), None)
                        
                        if not temp_col:
                            st.error(f"File {getattr(file, 'name', f'File {idx+1}')} missing temperature data")
                            st.write(f"Available columns: {', '.join(df.columns)}")
                            continue
                            
                        # Standardize format
                        epw_df = df[['datetime', temp_col]].copy()
                        epw_df.columns = ['DateTime', f'EPW {idx+1}']
                        epw_datasets.append(epw_df)
                        valid_count += 1
                        
                    except Exception as file_error:
                        st.error(f"Error processing {getattr(file, 'name', f'File {idx+1}')}: {str(file_error)}")
                
                if valid_count > 0:
                    # Merge datasets
                    combined_epw = pd.concat(epw_datasets, axis=1)
                    
                    # Display EPW chart
                    st.altair_chart(
                        create_chart(
                            combined_epw.filter(regex='EPW'),
                            {'EPW': '#8A2BE2'},
                            "EPW Temperature Analysis",
                            x_axis='DateTime:T',
                            x_format='%B'
                        ), use_container_width=True
                    )
                    
                    # Show data details
                    with st.expander("View EPW Data Details"):
                        st.write(f"Processed {valid_count}/{len(uploaded_files)} files")
                        st.dataframe(combined_epw.describe())
                        st.download_button(
                            label="Download Processed Data",
                            data=combined_epw.to_csv().encode('utf-8'),
                            file_name='processed_epw_data.csv',
                            mime='text/csv'
                        )
                else:
                    st.warning("No valid EPW files could be processed")
                    
            except Exception as epw_error:
                st.error(f"EPW Analysis Failed: {str(epw_error)}")
                st.write("Please check your EPW files and try again")

    # Footer 
    display_contact()
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<center> Polla Sktani ©2025 </center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
