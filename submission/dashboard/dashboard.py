import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set_theme(style='dark')

 # # # #

# import dataset
file_path = "/Users/kaysaazzahra/Documents/submission/dashboard/hour.csv"
hour_df = pd.read_csv(file_path)

file_path2 = "/Users/kaysaazzahra/Documents/submission/dashboard/day.csv"
day_df = pd.read_csv(file_path2)

# mengecek nilai kosong
hour_df.isna().sum()
day_df.isna().sum()

# mengecek duplikasi data
hour_df.duplicated().sum()

day_df.duplicated().sum()

# mengubah tipe data kolom date
def convert_to_datetime(dataframe, kolom_date):
    for column in kolom_date:
        dataframe[column] = pd.to_datetime(dataframe[column])

datetime_columns_hour = ["dteday"]
convert_to_datetime(hour_df, datetime_columns_hour)

datetime_columns_day = ["dteday"]
convert_to_datetime(day_df, datetime_columns_day)

# rename kolom
def rename_kolom(dataframe):
    renamed = {
        'weathersit': 'weather',
        'dteday': 'date',
        'yr': 'year',
        'mnth': 'month',
        'hr': 'hour',
        'hum': 'humidity',
        'cnt': 'count'
    }
    dataframe = dataframe.rename(columns=renamed)
    return dataframe

hour_df = rename_kolom(hour_df)
day_df = rename_kolom(day_df)

# Explore
# mencari nilai unik
hour_df.apply(lambda x: len(x.unique()))

# mengganti angka yang mewakili musim dengan label musim
season_rename = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
hour_df['season'] = hour_df['season'].map(season_rename)

# mengelompokkan dan menghitung jumlah peminjaman sepeda per musimnya
hour_df.groupby('season')['count'].sum().sort_values(ascending=False).head()

# mengubah kolom 'workingday' dan 'weekday' menjadi kategori
list_kolom = ['workingday', 'weekday']

for kolom in list_kolom:
  hour_df[kolom] = hour_df[kolom].astype('category')

# melihat peminjaman sepeda di tiap jamnya berdasarkan weekday dan weekend
hari_dan_jam = hour_df.groupby(['hour', 'weekday'])['count'].sum().reset_index()

# mengelompokan hari menjadi weekday (1, 2, 3, 4, 5) dan weekend (0 dan 6)
hour_df['weekday'] = hour_df['weekday'].map({0: 'Weekend', 6: 'Weekend', 1: 'Weekday', 2: 'Weekday', 3: 'Weekday', 4: 'Weekday', 5: 'Weekday'})

# mengelompokkan data berdasarkan tanggal dan menghitung total peminjaman perhari
pengguna_per_hari = day_df.groupby('date').sum().reset_index()

# menghitung rata-rata per hari
rata_rata_harian = pengguna_per_hari[['registered', 'casual']].mean()

# Visualisasi
# assign korelasi untuk digunakan sebagai sumbu y
jumlah_per_musim = hour_df.groupby('season')['count'].sum()

# urutkan berdasarkan jumlah tertinggi
jumlah_per_musim_sorted = jumlah_per_musim.sort_values(ascending=False)

# akan digunakan sebagai data
hari_dan_jam = hour_df.groupby(['hour', 'weekday'])['count'].sum().reset_index()


# Sidebar
with st.sidebar:
    # Menambahkan logo
    st.image("https://www.shutterstock.com/image-vector/bike-icon-vector-logo-template-600nw-1388480312.jpg")
    
    st.title("Enjoy Bike Company")


# Dashboard
st.header('Enjoy Bike Dashboard 🚲')

# Peminjaman sepeda berdasarkan musim
st.subheader('Grafik Peminjaman Sepeda Berdasarkan Musim')

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    x=jumlah_per_musim.index, y=jumlah_per_musim.values, 
    palette={'Spring':'lightblue', 'Summer':'lightblue', 'Fall':'darkblue', 'Winter':'lightblue'},
    order=jumlah_per_musim_sorted.index
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_yticks(range(0, 1200000, 100000))
ax.set_ylabel(None)
ax.set_xlabel("Musim", fontsize=30)
ax.set_title("Total Peminjaman", loc="center", fontsize=30)
ax.tick_params(axis='y', labelsize=23)
ax.tick_params(axis='x', labelsize=23)

st.pyplot(fig)

with st.expander("Description"):
    st.write(
        """Peminjaman terbanyak berada di musim gugur dengan urutan pertama, 
           diikuti dengan musim panas diurutan kedua, lalu musim dingin diurutan 
           ketiga dan diikuti oleh musim semi di urutan keempat. Terdapat perbedaan 
           jumlah yang cukup jauh di peminjaman sepeda pada musim gugur dan semi. 
           Sehingga dapat disimpulkan bahwa pengguna lebih memilih untuk meminjam 
           sepeda di musim gugur dibandingkan dengan di musim semi.
        """
    )

# Pola peminjaman sepeda di tiap jam berdasarkan weekday dan weekend
st.subheader('Grafik Peminjaman Sepeda di Tiap Jam')

fig, ax = plt.subplots(figsize=(20, 10))
sns.lineplot(
    data=hari_dan_jam, 
    x='hour', 
    y='count', 
    hue='weekday'
)

ax.set_title("Weekday vs Weekend", loc="center", fontsize=30)

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

ax.set_yticks(range(0, 300000, 25000))
ax.set_ylabel("Total Peminjaman", fontsize=30)


ax.set_xlabel("Hour", fontsize=30)
ax.set_xticks(range(24), labels=[str(i) for i in range(24)])

st.pyplot(fig)

with st.expander("Description"):
    st.write(
        """Peminjaman sepeda memiliki peminat jauh lebih tinggi di weekday 
        dibandingkan dengan weekend. Puncak tertinggi saat weekend hanya berada 
        di range 50000-75000 pada jam 13. Sementara puncak tertinggi saat 
        weekday menyentuh range 250000-275000 pada jam 17. Selain itu puncak 
        tertinggi kedua saat weekday ada di jam 8 dengan range peminjaman 
        225000-250000. Hal ini mungkin disebabkan pada saat weekend pengguna 
        cenderung lebih bersantai dan aktif di siang hari. Sementara pada saat 
        weekday penggunaan di jam 8 dan 17 yang merupakan dua titik tertinggi 
        dapat disebabkan karena aktivitas sehari-hari yaitu bekerja.
        """
    )


# Rata-rata distribusi harian berdasarkan kategori pengguna
st.subheader('Rata-rata Distribusi Harian Peminjaman Sepeda')

fig, ax = plt.subplots(figsize=(14, 7))
sns.barplot(
   x=rata_rata_harian.index, y=rata_rata_harian.values,
   palette={'registered':'darkblue', 'casual':'lightblue'}
)

ax.set_title("Register vs Casual", loc="center", fontsize=25)

ax.tick_params(axis='y', labelsize=17)
ax.tick_params(axis='x', labelsize=17)

ax.set_yticks(range(0, 4000, 200))
ax.set_ylabel('Rata-rata Peminjaman', fontsize=20)


ax.set_xlabel('Pengguna', fontsize=20)

st.pyplot(fig)

with st.expander("Description"):
    st.write(
        """Perbedaan signifikan dapat dilihat dari rata-rata distribusi harian 
        peminjaman sepeda. Mayoritas peminjam ialah mereka yang sudah menjadi 
        pengguna terdaftar dengan rata-rata harian berada di angka 3600. 
        Sedangkan untuk pengguna casual sendiri memiliki rata-rata pengguna 
        sebanyak kurang lebih 800. Dapat disimpulkan bahwa pengguna harian mayoritas 
        adalah pengguna yang sudah terdaftar.
        """
    )

    