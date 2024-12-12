# Assumes the combined data (CSV) is already available
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Menentukan path relatif dari root repository
combined_path = "C:/Users/Lenovo/Downloads/submission/dashboard/combined_data.csv"

# Membaca file
combined_df = pd.read_csv(combined_path)

# Set Streamlit page layout
st.set_page_config(
    page_title="Bike Sharing Analysis Dashboard",
    layout="wide",
)

# Dashboard title
st.title("🚴Bike Sharing Data Analysis Dashboard")
st.markdown("### Explore key trends and insights from bike-sharing data.")

# Sidebar filters
st.sidebar.header("Filters")
season_filter = st.sidebar.multiselect(
    "Select Season (1: Spring, 2: Summer, 3: Fall, 4: Winter)",
    options=combined_df['season'].unique(),
    default=combined_df['season'].unique()
)
workingday_filter = st.sidebar.radio(
    "Filter by Working Day (0: No, 1: Yes):",
    options=combined_df['workingday'].unique(),
    index=0
)

filtered_df = combined_df[
    (combined_df['season'].isin(season_filter)) &
    (combined_df['workingday'] == workingday_filter)
]

# Tabs for analysis
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Seasonal Impact", "Hourly Trends", "Weather Impact", "Temperature Effect", "Weekday vs Weekend"]
)

# Tab 1: Impact of season on bike usage
with tab1:
    st.subheader("Impact of Season on Bike Usage")
    season_counts = filtered_df.groupby('season')['cnt_day'].mean()
    fig, ax = plt.subplots(figsize=(8, 5))
    season_counts.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title('Average Bike Usage by Season')
    ax.set_xlabel('Season (1: Spring, 2: Summer, 3: Fall, 4: Winter)')
    ax.set_ylabel('Average Count')
    st.pyplot(fig)

# Tab 2: Hourly trends in bike usage
with tab2:
    st.subheader("Hourly Trends in Bike Usage")
    hourly_counts = combined_df.groupby('hr')['cnt_hour'].mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    hourly_counts.plot(kind='line', marker='o', color='orange', ax=ax)
    ax.set_title('Average Bike Usage by Hour')
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Average Count')
    st.pyplot(fig)

# Tab 3: Weather conditions and bike usage
with tab3:
    st.subheader("Effect of Weather Conditions on Bike Usage")
    weather_counts = filtered_df.groupby('weathersit')['cnt_day'].mean()
    fig, ax = plt.subplots(figsize=(8, 5))
    weather_counts.plot(kind='bar', color='lightgreen', ax=ax)
    ax.set_title('Average Bike Usage by Weather Condition')
    ax.set_xlabel('Weather (1: Clear, 2: Misty, 3: Light Snow/Rain)')
    ax.set_ylabel('Average Count')
    st.pyplot(fig)

# Tab 4: Relationship between temperature and bike usage
with tab4:
    st.subheader("Relationship Between Temperature and Bike Usage")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x=filtered_df['temp_day'], y=filtered_df['cnt_day'], color='purple', ax=ax)
    sns.regplot(x=filtered_df['temp_day'], y=filtered_df['cnt_day'], scatter=False, color='red', ax=ax)
    ax.set_title('Relationship Between Temperature and Bike Usage')
    ax.set_xlabel('Temperature (Normalized)')
    ax.set_ylabel('Bike Count')
    st.pyplot(fig)

# Tab 5: Weekday vs Weekend usage
with tab5:
    st.subheader("Difference in Bike Usage on Weekdays vs Weekends")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x='workingday', y='cnt_day', data=filtered_df, palette='Set2', ax=ax)
    ax.set_title('Bike Usage: Working Day vs Non-Working Day')
    ax.set_xlabel('Working Day (0: No, 1: Yes)')
    ax.set_ylabel('Count')
    st.pyplot(fig)

# Footer
st.markdown("### Key Takeaways")
st.markdown("""
- **Seasonal Impact**: Usage is highest during Fall and Summer due to favorable weather.
- **Hourly Trends**: Peaks are observed during commuting hours (8 AM and 5 PM).
- **Weather Conditions**: Clear weather sees the highest usage, while mist and rain reduce usage.
- **Temperature Effect**: Usage increases with temperature but drops at extreme temperatures.
- **Weekdays vs Weekends**: Weekends show higher usage due to recreational activities.
""")
st.sidebar.info('Dashboard by Yesa Devina Reza :sparkles:')




