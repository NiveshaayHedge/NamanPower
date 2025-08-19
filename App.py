import streamlit as st
from playwrightCode import fetch_pib_links
import time
import pandas as pd
import io
from datetime import datetime, timedelta

st.set_page_config(layout="wide", page_title="Power Sector Dashboard", page_icon="⚡")

def apply_custom_css():
    st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #2c3e50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #34495e;
        transform: translateY(-2px);
    }
    .stSelectbox {
        background-color: white;
        border-radius: 8px;
        padding: 5px;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .title {
        color: #2c3e50;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .subtitle {
        color: #7f8c8d;
        font-size: 16px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def main():
    apply_custom_css()
    
    # Get yesterday's date
    yesterday = datetime.now() - timedelta(days=1)
    default_month = yesterday.month

    # Header
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown('<div class="title">⚡ Power Sector Dashboard</div>', unsafe_allow_html=True)
            st.markdown('<div class="subtitle">Real-time insights and data analysis</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div style="text-align: right; color: #7f8c8d;">Last updated: {datetime.now().strftime("%Y-%m-%d")}</div>', 
                       unsafe_allow_html=True)

    # Selection Card
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Data for dropdowns
        day_option = ["All"] + list(range(1, 32))
        years = list(range(2025, 2016, -1))
        month_mapping = {
            "January": "1", "February": "2", "March": "3", "April": "4", "May": "5", "June": "6",
            "July": "7", "August": "8", "September": "9", "October": "10", "November": "11", "December": "12"
        }
        month_names = list(month_mapping.keys())
        
        # Set default month index
        default_month_index = default_month - 1  # Subtract 1 because index starts at 0

        col1, col2, col3 = st.columns(3)
        
        with col1:
            day = st.selectbox("📅 Select Day", 
                             options=day_option,
                             index=0,  # Default to "All"
                             help="Choose a specific day or all days")
        with col2:
            selected_month = st.selectbox("🗓️ Select Month", 
                                        month_names,
                                        index=default_month_index,  # Default to yesterday's month
                                        help="Choose the month of interest")
        with col3:
            year = st.selectbox("📆 Select Year", 
                              years,
                              index=0,  # Default to 2025
                              help="Choose the year of interest")

        fetch_col, _ = st.columns([1, 5])
        with fetch_col:
            fetch_button = st.button("🚀 Fetch Data", use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    if fetch_button:
        day_value = "0" if day == "All" else str(day)
        month_value = month_mapping[selected_month]
        year_value = str(year)

        with st.container():
            with st.spinner("🔄 Fetching data... Please wait!"):
                result = fetch_pib_links(day_value, month_value, year_value)

            if result:
                df = pd.DataFrame(result)
                if 'keywords' in df.columns:
                    df['keywords'] = df['keywords'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
                
                st.markdown('<div class="card">', unsafe_allow_html=True)
                
                st.success("✅ Data retrieved successfully!")
                st.dataframe(
                    df,
                    use_container_width=True,
                    height=400,
                    column_config={
                        "title": st.column_config.TextColumn("Title", width="large"),
                        "url": st.column_config.LinkColumn("URL", width="large"),
                        "date": st.column_config.TextColumn("Date", width="medium"),
                        "keywords": st.column_config.TextColumn("Keywords", width="medium")
                    }
                )

                csv_data = convert_df_to_csv(df)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name=f"power_sector_data_{day_value}_{month_value}_{year_value}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    help="Download the data as a CSV file"
                )
                
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("❌ No data available for the selected period")
                st.markdown(
                    '<div style="color: #7f8c8d; text-align: center;">Try adjusting your date selection</div>',
                    unsafe_allow_html=True
                )

if __name__ == "__main__":
    main()



