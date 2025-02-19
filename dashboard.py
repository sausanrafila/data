import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Load data
merged_df = pd.read_csv("merged_df.csv")

# Pastikan kolom yang dibutuhkan ada dan tidak memiliki nilai NaN
required_columns = ["season", "cnt", "weekday", "hr", "temp", "hum", "windspeed"]
for col in required_columns:
    if col not in merged_df.columns:
        st.error(f"Kolom {col} tidak ditemukan dalam dataset")
    elif merged_df[col].isnull().sum() > 0:
        st.warning(f"Kolom {col} memiliki {merged_df[col].isnull().sum()} nilai kosong, akan diisi dengan median.")
        merged_df[col].fillna(merged_df[col].median(), inplace=True)

# Menghapus duplikasi jika ada
duplicates = merged_df.duplicated().sum()
if duplicates > 0:
    st.warning(f"Ditemukan {duplicates} baris duplikat, akan dihapus.")
    merged_df = merged_df.drop_duplicates()

# Memastikan tipe data benar
merged_df["weekday"] = merged_df["weekday"].astype(int)
merged_df["hr"] = merged_df["hr"].astype(int)
merged_df["season"] = merged_df["season"].astype(int)
merged_df["cnt"] = merged_df["cnt"].astype(int)

# Mapping untuk musim jika season dimulai dari 1
season_dict = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
if merged_df["season"].min() == 0:
    season_dict = {0: "Spring", 1: "Summer", 2: "Fall", 3: "Winter"}  # Jika indeks mulai dari 0
merged_df["season_name"] = merged_df["season"].map(season_dict)

# Mapping weekday ke nama hari
weekday_dict = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
merged_df["weekday_name"] = merged_df["weekday"].map(weekday_dict)

# Judul Dashboard
st.title("🚴‍♂️ Dashboard Analisis Penggunaan Sepeda")

# **📊 Visualisasi 1: Pola Penyewaan Sepeda Berdasarkan Musim**
st.subheader("Jumlah Penyewaan Sepeda per Musim")
fig, ax = plt.subplots()
merged_df.groupby("season_name")["cnt"].sum().plot(kind="bar", ax=ax, color='skyblue')
ax.set_title("Total Penyewaan Sepeda per Musim")
st.pyplot(fig)

# **📊 Visualisasi 2: Pola Penyewaan Sepeda per Hari dalam Seminggu**
st.subheader("Pola Penyewaan Sepeda per Hari dalam Seminggu")
fig, ax = plt.subplots()
merged_df.groupby("weekday_name")["cnt"].sum().plot(kind="bar", ax=ax, color='lightcoral')
ax.set_title("Jumlah Penyewaan Sepeda per Hari dalam Seminggu")
st.pyplot(fig)

# **📊 Visualisasi 3: Pola Penyewaan Sepeda per Jam**
st.subheader("Rata-rata Penyewaan Sepeda per Jam")
fig, ax = plt.subplots()
merged_df.groupby("hr")["cnt"].mean().plot(kind="bar", ax=ax, color='lightgreen')
ax.set_title("Rata-rata Penyewaan Sepeda per Jam")
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig)

# **📊 Visualisasi 4: Pengaruh Cuaca terhadap Penyewaan Sepeda**
st.subheader("Pengaruh Suhu, Kelembaban, dan Kecepatan Angin terhadap Penyewaan Sepeda")

# Scatter plot untuk suhu
fig, ax = plt.subplots()
ax.scatter(merged_df["temp"], merged_df["cnt"], alpha=0.5, color='blue')
ax.set_title("Hubungan Suhu dengan Penyewaan Sepeda")
ax.set_xlabel("Suhu")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# Scatter plot untuk kelembaban
fig, ax = plt.subplots()
ax.scatter(merged_df["hum"], merged_df["cnt"], alpha=0.5, color='red')
ax.set_title("Hubungan Kelembaban dengan Penyewaan Sepeda")
ax.set_xlabel("Kelembaban")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# Scatter plot untuk kecepatan angin
fig, ax = plt.subplots()
ax.scatter(merged_df["windspeed"], merged_df["cnt"], alpha=0.5, color='green')
ax.set_title("Hubungan Kecepatan Angin dengan Penyewaan Sepeda")
ax.set_xlabel("Kecepatan Angin")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# Kesimpulan
st.markdown("""
### **Kesimpulan:**
✅ Penyewaan sepeda **terbanyak pada musim Fall (Gugur)**, sedangkan **terendah pada Winter (Dingin)**.  
✅ Hari kerja cenderung memiliki penyewaan lebih stabil dibanding akhir pekan.  
✅ Penyewaan puncaknya terjadi **pada jam sibuk pagi (07:00-09:00) dan sore (17:00-19:00)**.  
✅ Suhu yang lebih tinggi cenderung meningkatkan jumlah penyewaan, sedangkan kelembaban dan kecepatan angin yang tinggi berpotensi menurunkannya.
""")
