import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur konfigurasi halaman
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    
    day_df = pd.read_csv('dashboard/day_cleaned.csv')
    hour_df = pd.read_csv('dashboard/hour_cleaned.csv')
    
    # Memastikan kolom 'date' dalam format datetime
    day_df['date'] = pd.to_datetime(day_df['date'])
    hour_df['date'] = pd.to_datetime(hour_df['date'])
    
    return day_df, hour_df

day_df, hour_df = load_data()


# Mendapatkan tanggal minimum dan maksimum untuk input
min_date = day_df['date'].min()
max_date = day_df['date'].max()

with st.sidebar:
    st.title("Filter Data")
    # Widget untuk memilih rentang waktu
    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Memfilter dataframe berdasarkan rentang waktu yang dipilih
main_df = day_df[(day_df['date'] >= pd.to_datetime(start_date)) & 
                 (day_df['date'] <= pd.to_datetime(end_date))]

main_hour_df = hour_df[(hour_df['date'] >= pd.to_datetime(start_date)) & 
                       (hour_df['date'] <= pd.to_datetime(end_date))]


# 1. Header
st.header('Bike Sharing Dashboard')
st.markdown('**by Yayan Kurniawan**')

# 2. KPI Section (Menggunakan main_df yang sudah difilter)
st.subheader('Key Performance Indicators')
col1, col2, col3 = st.columns(3)

with col1:
    total_riders = main_df['count'].sum()
    st.metric("Total Riders", value=f"{total_riders:,}")

with col2:
    total_casual = main_df['casual'].sum()
    st.metric("Total Casual Riders", value=f"{total_casual:,}")

with col3:
    total_registered = main_df['registered'].sum()
    st.metric("Total Registered Riders", value=f"{total_registered:,}")

st.divider()

# Layout untuk visualisasi
col_left, col_right = st.columns(2)

with col_left:
    # 3. Peminjaman tertinggi berdasarkan hari
    st.subheader('Peminjaman Berdasarkan Hari')
    weekday_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    day_count = main_df.groupby('weekday')['count'].sum().reindex(weekday_order).reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='weekday', y='count', data=day_count, palette='viridis', ax=ax)
    ax.set_xlabel('Hari')
    ax.set_ylabel('Total Peminjaman')
    st.pyplot(fig)

    # 4. Pengaruh Cuaca
    st.subheader('Pengaruh Cuaca Terhadap Peminjaman')
    weather_count = main_df.groupby('weather')['count'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='weather', y='count', data=weather_count, palette='coolwarm', ax=ax)
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Rata-rata Peminjaman')
    st.pyplot(fig)

with col_right:
    # 5. Hari Kerja vs Hari Libur
    st.subheader('Hari Kerja vs Bukan Hari Kerja')
    workday_count = main_df.groupby('workingday')['count'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='workingday', y='count', data=workday_count, palette='Set2', ax=ax)
    ax.set_xlabel('Status Hari')
    ax.set_ylabel('Rata-rata Peminjaman')
    st.pyplot(fig)

    # 6. Musim dengan rata-rata tertinggi
    st.subheader('Rata-rata Peminjaman Berdasarkan Musim')
    season_count = main_df.groupby('season')['count'].mean().reset_index().sort_values(by='count', ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='season', y='count', data=season_count, palette='magma', ax=ax)
    ax.set_xlabel('Musim')
    ax.set_ylabel('Rata-rata Peminjaman')
    st.pyplot(fig)

# 7. Jam dengan peminjaman tertinggi (Full Width)
st.divider()
st.subheader('Tren Peminjaman Berdasarkan Jam')
hour_count = main_hour_df.groupby('hour')['count'].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(x='hour', y='count', data=hour_count, marker='o', color='royalblue', ax=ax)
ax.set_xticks(range(0, 24))
ax.set_xlabel('Jam (0-23)')
ax.set_ylabel('Rata-rata Peminjaman')
ax.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig)

st.caption('Copyright (c) Yayan Kurniawan 2026')