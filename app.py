import streamlit as st
import pandas as pd
import altair as alt
# UPDATE IMPORT LINE
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
    
    chart = alt.Chart(df_melted).mark_line(
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
    return chart

@st.cache_data
def load_erbil_data():
    data = pd.concat([
        load_baseline().rename(columns={'Temperature': '2023 Baseline'}),
        load_2050().rename(columns={'Temperature': '2050 Projection'}),
        load_2080().rename(columns={'Temperature': '2080 Projection'})
    ], axis=1)
    data.index = pd.to_datetime(data.index)
    return data

def main():
    st.set_page_config(page_title="Climate Analysis", layout="wide")
    st.title("Climate Data Visualization")
    
    # Load data
    erbil_data = load_erbil_data()
    uploaded_files = display_sidebar()
    custom_data = {}
    
    if uploaded_files:
        for file in uploaded_files:
            custom_data[file.name] = read_epw(file)['Temperature']
    
    # Original Chart 1
    st.header("Erbil Climate Scenarios")
    selected_erbil = []
    cols = st.columns(3)
    scenarios = list(ERBIL_COLORS.keys())
    for i, col in enumerate(cols):
        with col:
            if st.checkbox(scenarios[i], value=True, key=f"erbil_{i}"):
                selected_erbil.append(scenarios[i])
    
    if selected_erbil:
        st.altair_chart(
            create_chart(
                erbil_data[selected_erbil],
                {k: v for k, v in ERBIL_COLORS.items() if k in selected_erbil},
                "Erbil Temperature Projections"
            ),
            use_container_width=True
        )
    else:
        st.warning("Please select at least one Erbil scenario")
    
    # Original Chart 2
    if custom_data:
        st.header("Uploaded Climate Files")
        custom_df = pd.concat(custom_data.values(), axis=1)
        custom_df.columns = custom_data.keys()
        st.altair_chart(
            create_chart(
                custom_df,
                {name: '#FFA500' for name in custom_data.keys()},
                "Uploaded Temperature Data"
            ),
            use_container_width=True
        )
    
    # Original Chart 3 (Monthly Analysis)
    st.header("Monthly Temperature Analysis (Erbil)")
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
                f"Hourly Temperature Trends for {pd.Timestamp(2023, month, 1).strftime('%B')}",
                x_axis='DateTime:T',
                x_format='%d'
            ),
            use_container_width=True
        )
    else:
        st.warning("No data available for the selected month.")
    
    # NEW CHART 4: Hours Above Threshold
    st.header("Extreme Heat Hours Analysis")
    
    # Add threshold control to sidebar
    with st.sidebar:
        st.markdown("---")
        threshold = st.number_input(
            "🌡️ Temperature Threshold (°C)",
            min_value=30,
            max_value=60,
            value=40,
            step=1,
            help="Analyze hours above this temperature"
        )
    
    # Calculate hours above threshold
    hours_data = {
        '2023 Baseline': count_hours_above_threshold(load_baseline(), threshold),
        '2050 Projection': count_hours_above_threshold(load_2050(), threshold),
        '2080 Projection': count_hours_above_threshold(load_2080(), threshold)
    }
    
    # Create bar chart
    df_hours = pd.DataFrame({
        'Scenario': list(hours_data.keys()),
        'Hours': list(hours_data.values())
    })
    
    chart = alt.Chart(df_hours).mark_bar().encode(
        x=alt.X('Scenario:N', title='', sort=list(ERBIL_COLORS.keys())),
        y=alt.Y('Hours:Q', title='Hours Above Threshold'),
        color=alt.Color('Scenario:N').scale(
            domain=list(ERBIL_COLORS.keys()),
            range=list(ERBIL_COLORS.values())
        ),
        tooltip=['Scenario', alt.Tooltip('Hours:Q', title='Hours')]
    ).properties(
        height=400,
        title=f"Annual Hours Above {threshold}°C"
    )
    
    st.altair_chart(chart, use_container_width=True)
    
    # Footer
    display_contact()
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<center> Polla Sktani ©2025 </center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
