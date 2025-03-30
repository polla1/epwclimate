import streamlit as st
import pandas as pd
import altair as alt
from database import load_baseline, load_2050, load_2080, read_epw
from sidebar import display_sidebar
from contact import display_contact

# Color configuration
ERBIL_COLORS = {
    '2023 Baseline': '#00FF00',  # Green
    '2050 Projection': '#0000FF',  # Blue
    '2080 Projection': '#FF0000'  # Red
}
UPLOAD_COLORS = ['#FFA500', '#800080', '#00FFFF']  # Distinct colors for uploads

def create_chart(data, colors, title):
    """Create an interactive line chart with consistent styling"""
    df_melted = data.reset_index().melt(
        id_vars=['DateTime'],
        var_name='Scenario',
        value_name='Temperature'
    )
    
    return alt.Chart(df_melted).mark_line(
        opacity=0.7,
        strokeWidth=2
    ).encode(
        x=alt.X('DateTime:T', title='Date', axis=alt.Axis(format='%b %Y')),
        y=alt.Y('Temperature:Q', title='Temperature (°C)', scale=alt.Scale(zero=False)),
        color=alt.Color('Scenario:N').scale(
            domain=list(colors.keys()),
            range=list(colors.values())
        ),
        tooltip=[
            'Scenario',
            alt.Tooltip('DateTime:T', title='Date', format='%B %d, %Y'),
            alt.Tooltip('Temperature:Q', format='.1f°C')
        ]
    ).properties(
        height=400,
        title=alt.TitleParams(
            text=title,
            fontSize=20,
            anchor='start'
        )
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )

@st.cache_data(show_spinner="Loading climate data...")
def load_erbil_data():
    """Load and validate Erbil climate data"""
    try:
        baseline = load_baseline()
        proj_2050 = load_2050()
        proj_2080 = load_2080()
        
        # Validate data consistency
        if not all(len(df) == 8760 for df in [baseline, proj_2050, proj_2080]):
            st.error("Invalid data: EPW files should contain full year hourly data")
            st.stop()
            
        return pd.concat([
            baseline.rename(columns={'Temperature': '2023 Baseline'}),
            proj_2050.rename(columns={'Temperature': '2050 Projection'}),
            proj_2080.rename(columns={'Temperature': '2080 Projection'})
        ], axis=1)
        
    except Exception as e:
        st.error(f"Failed to load climate data: {str(e)}")
        st.stop()

def handle_uploads(uploaded_files):
    """Process uploaded files with error handling"""
    custom_data = {}
    for idx, file in enumerate(uploaded_files):
        try:
            df = read_epw(file)
            custom_data[f"{file.name} ({idx+1})"] = df['Temperature']
        except Exception as e:
            st.error(f"Error processing {file.name}: {str(e)}")
    return custom_data

def main():
    st.set_page_config(page_title="Climate Analysis", layout="wide")
    st.title("Erbil Climate Scenario Visualizer")
    
    # Load core data
    erbil_data = load_erbil_data()
    
    # Handle uploads
    uploaded_files = display_sidebar()
    custom_data = handle_uploads(uploaded_files)

    # Main visualization section
    with st.container():
        st.header("Erbil Climate Scenarios Comparison")
        
        # Scenario selector
        selected = st.multiselect(
            "Select scenarios to display:",
            options=list(ERBIL_COLORS.keys()),
            default=list(ERBIL_COLORS.keys()),
            format_func=lambda x: f"{x} {'✓' if x in selected else ''}"
        )
        
        if selected:
            chart = create_chart(
                erbil_data[selected],
                {k: ERBIL_COLORS[k] for k in selected},
                "Temperature Projections for Erbil, Iraq"
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("Please select at least one scenario")

    # Uploaded files visualization
    if custom_data:
        with st.container():
            st.header("Custom Climate Data Analysis")
            custom_df = pd.concat(custom_data.values(), axis=1)
            custom_df.columns = custom_data.keys()
            
            upload_colors = {name: UPLOAD_COLORS[i % len(UPLOAD_COLORS)] 
                           for i, name in enumerate(custom_data.keys())}
            
            st.altair_chart(
                create_chart(
                    custom_df,
                    upload_colors,
                    "Uploaded Temperature Data Comparison"
                ),
                use_container_width=True
            )

    # Enhanced monthly analysis
    with st.container():
        st.header("Detailed Monthly Analysis")
        col1, col2 = st.columns([1, 3])
        
        with col1:
            month = st.selectbox(
                "Select Month:", 
                range(1, 13), 
                format_func=lambda x: pd.Timestamp(2023, x, 1).strftime('%B'),
                help="Select a month to view daily temperature variations"
            )
            
            show_stats = st.checkbox("Show monthly statistics", value=True)

        with col2:
            monthly_data = erbil_data[erbil_data.index.month == month]
            
            if not monthly_data.empty:
                st.altair_chart(
                    create_chart(
                        monthly_data,
                        ERBIL_COLORS,
                        f"Daily Temperatures for {pd.Timestamp(2023, month, 1).strftime('%B')}"
                    ),
                    use_container_width=True
                )
                
                if show_stats:
                    stats = monthly_data.describe().T
                    st.dataframe(
                        stats.style.format("{:.1f}°C"),
                        use_container_width=True
                    )
            else:
                st.warning("No data available for selected month")

    display_contact()

if __name__ == "__main__":
    main()
