import streamlit as st
import pandas as pd
import altair as alt
from database import load_baseline, load_2050, load_2080, read_epw
from sidebar import display_sidebar
from contact import display_contact

ERBIL_COLORS = {
    '2023 Baseline': '#00FF00',
    '2050 Projection': '#0000FF',
    '2080 Projection': '#FF0000'
}

def create_chart(data, colors, title):
    df_melted = data.reset_index().melt(
        id_vars=['DateTime'],
        var_name='Scenario',
        value_name='Temperature'
    )
    
    return alt.Chart(df_melted).mark_line(opacity=0.7, strokeWidth=2).encode(
        x=alt.X('DateTime:T', title='Date'),
        y=alt.Y('Temperature:Q', title='Temperature (°C)'),
        color=alt.Color('Scenario:N').scale(domain=list(colors.keys()), 
        tooltip=['Scenario', alt.Tooltip('Temperature:Q', format='.1f')]
    ).properties(height=400, title=title)

@st.cache_data
def load_erbil_data():
    return pd.concat([
        load_baseline().rename(columns={'Temperature': '2023 Baseline'}),
        load_2050().rename(columns={'Temperature': '2050 Projection'}),
        load_2080().rename(columns={'Temperature': '2080 Projection'})
    ], axis=1)

def main():
    st.set_page_config(page_title="Climate Analysis", layout="wide")
    st.title("Climate Data Visualization")
    
    erbil_data = load_erbil_data()
    uploaded_files = display_sidebar()
    custom_data = {file.name: read_epw(file)['Temperature'] for file in uploaded_files}

    st.header("Weather file (.EPW) Scenarios of Erbil")
    selected_erbil = [scenario for i, scenario in enumerate(ERBIL_COLORS) 
                     if st.checkbox(scenario, True, key=f"erbil_{i}")]
    
    if selected_erbil:
        st.altair_chart(create_chart(erbil_data[selected_erbil], 
                       {k: v for k, v in ERBIL_COLORS.items() if k in selected_erbil},
                       "Interactive Yearly Temperature Projections"), 
                       use_container_width=True)
    
    if custom_data:
        st.header("Uploaded Climate Files")
        custom_df = pd.concat(custom_data.values(), axis=1)
        st.altair_chart(create_chart(custom_df, 
                                    {name: '#FFA500' for name in custom_data.keys()},
                                    "Uploaded Temperature Data"), 
                                    use_container_width=True)

    st.header("Monthly Temperature Analysis (Erbil)")
    month = st.selectbox("Select Month", range(1,13), 
                        format_func=lambda x: pd.Timestamp(2023, x, 1).strftime('%B'))
    st.line_chart(erbil_data[erbil_data.index.month == month], use_container_width=True)
    
    display_contact()

if __name__ == "__main__":
    main()
