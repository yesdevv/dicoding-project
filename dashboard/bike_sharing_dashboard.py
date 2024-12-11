# Assumes the combined data (CSV) is already available
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load combined dataset from local file (pre-exported from Google Colab)
combined_df = pd.read_csv('C:/Users/Lenovo/Downloads/submission/dashboard/combined_data.csv')
combined_df['dteday'] = pd.to_datetime(combined_df['dteday'])

# Title
st.title("🚴 Dashboard Interaktif Bike Sharing")

# Sidebar Filters
st.sidebar.header("Filter Data")
seasons = st.sidebar.multiselect(
    "Pilih Musim:",
    options=[1, 2, 3, 4],
    default=[1, 2, 3, 4],
    format_func=lambda x: {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}[x],
)
working_day = st.sidebar.selectbox(
    "Hari Kerja atau Libur:",
    options=["Semua", "Hari Kerja", "Hari Libur"],
    index=0,
)
start_date = st.sidebar.date_input(
    "Pilih Tanggal Mulai:",
    min_value=combined_df['dteday'].min(),
    max_value=combined_df['dteday'].max(),
    value=combined_df['dteday'].min(),
)
end_date = st.sidebar.date_input(
    "Pilih Tanggal Akhir:",
    min_value=combined_df['dteday'].min(),
    max_value=combined_df['dteday'].max(),
    value=combined_df['dteday'].max(),
)

# Filter the dataset based on the selected options
filtered_df = combined_df[
    (combined_df['season'].isin(seasons)) &
    (combined_df['dteday'] >= pd.to_datetime(start_date)) &
    (combined_df['dteday'] <= pd.to_datetime(end_date))
]

if working_day == "Hari Kerja":
    filtered_df = filtered_df[filtered_df['workingday'] == 1]
elif working_day == "Hari Libur":
    filtered_df = filtered_df[filtered_df['workingday'] == 0]

# Tabs for visualizations
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Distribusi Penggunaan", "Pengaruh Musim", "Jam Sibuk", "Suhu", "Korelasi Data"]
)

# 1. Distribusi Penggunaan Sepeda
with tab1:
    st.subheader("Distribusi Penggunaan Sepeda Harian")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(filtered_df['cnt_day'], bins=30, kde=True, color='blue', ax=ax)
    ax.set_title("Distribusi Penggunaan Sepeda")
    ax.set_xlabel("Jumlah Pengguna")
    ax.set_ylabel("Frekuensi")
    st.pyplot(fig)
  
# 2. Pengaruh Musim
with tab2:
    st.subheader("Rata-Rata Penggunaan Sepeda per Musim")
    fig, ax = plt.subplots(figsize=(10, 6))
    season_counts = filtered_df.groupby('season')['cnt_day'].mean()
    season_counts.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title("Rata-Rata Penggunaan Sepeda per Musim")
    ax.set_xlabel("Musim (1: Spring, 2: Summer, 3: Fall, 4: Winter)")
    ax.set_ylabel("Rata-Rata Jumlah Pengguna")
    plt.xticks(rotation=0) 
    st.pyplot(fig)

# 3. Jam Sibuk
with tab3:
    st.subheader("Jam Sibuk dalam Sehari")
    combined_df['hr'] = pd.to_datetime(combined_df['dteday']).dt.hour
    hour_to_filter = st.slider('Pilih Jam:', 0, 23, (0, 23))
    hourly_filtered = filtered_df[(filtered_df['hr'] >= hour_to_filter[0]) & (filtered_df['hr'] <= hour_to_filter[1])]
    hourly_counts = hourly_filtered.groupby('hr')['cnt_hour'].mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    hourly_counts.plot(kind='line', marker='o', color='orange', ax=ax)
    ax.set_title("Rata-Rata Penggunaan Sepeda per Jam")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-Rata Jumlah Pengguna")
    st.pyplot(fig)

# 4. Suhu
with tab4:
    st.subheader("Hubungan Suhu terhadap Penggunaan Sepeda")
    temp_range = st.slider("Pilih Rentang Suhu:",
                           float(filtered_df['temp_day'].min()),
                           float(filtered_df['temp_day'].max()),
                           (float(filtered_df['temp_day'].min()), float(filtered_df['temp_day'].max())))
    temp_filtered = filtered_df[filtered_df['temp_day'].between(temp_range[0], temp_range[1])]
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x=temp_filtered['temp_day'], y=temp_filtered['cnt_day'], color='purple', ax=ax)
    sns.regplot(x=temp_filtered['temp_day'], y=temp_filtered['cnt_day'], scatter=False, color='red', ax=ax)
    ax.set_title("Hubungan Suhu dengan Penggunaan Sepeda")
    ax.set_xlabel("Suhu (Normalisasi)")
    ax.set_ylabel("Jumlah Pengguna")
    st.pyplot(fig)

# 5. Korelasi Data
with tab5:
    st.subheader("Korelasi Antar Variabel")
    fig, ax = plt.subplots(figsize=(12, 8))
    correlation = filtered_df.corr()
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
    ax.set_title("Heatmap Korelasi Variabel")
    st.pyplot(fig)

# Footer
st.sidebar.info('Dashboard by Yesa Devina Reza :sparkles:')