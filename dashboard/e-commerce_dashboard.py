import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Memuat dataset yang telah dibersihkan dan diproses
df_order_items = pd.read_csv('../data/order_items_dataset.csv')
df_order_reviews = pd.read_csv('../data/order_reviews_dataset.csv')
df_products = pd.read_csv('../data/products_dataset.csv')

# Gabungkan dataset untuk analisis lebih lanjut
df_cleaned = pd.merge(df_order_items, df_products[['product_id', 'product_category_name']], on='product_id', how='left')
df_cleaned = pd.merge(df_cleaned, df_order_reviews[['order_id', 'review_score']], on='order_id', how='left')
df_cleaned = df_cleaned.dropna(subset=['review_score'])

# Menambahkan judul dan deskripsi dashboard
st.title('E-Commerce Data Analysis Dashboard')
st.markdown('Ini adalah dashboard interaktif yang menunjukkan analisis dari dataset e-commerce yang berfokus pada pembelian produk dan rating pelanggan.')

# Analisis kategori produk yang paling sering dibeli
category_counts = df_cleaned['product_category_name'].value_counts()

# Membuat grafik bar untuk kategori produk yang paling sering dibeli
st.subheader('Jumlah Pembelian Berdasarkan Kategori Produk')
fig, ax = plt.subplots(figsize=(10, 6))
category_counts.plot(kind='bar', ax=ax)
plt.title('Jumlah Pembelian Berdasarkan Kategori Produk')
plt.xlabel('Kategori Produk')
plt.ylabel('Jumlah Pembelian')
plt.xticks(rotation=45)
st.pyplot(fig)

# Menghitung frekuensi dan rating produk
product_frequency = df_cleaned['product_id'].value_counts()
average_rating = df_cleaned.groupby('product_id')['review_score'].mean()

# Menggabungkan frekuensi dan rating dalam satu dataframe
product_analysis = pd.DataFrame({
    'frequency': product_frequency,
    'average_rating': average_rating
}).reset_index()

# Membuat grafik hubungan antara rating dan frekuensi pembelian
st.subheader('Hubungan Antara Rating Produk dan Frekuensi Pembelian')
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(x='average_rating', y='frequency', data=product_analysis, ax=ax)
plt.title('Hubungan antara Rating Produk dan Frekuensi Pembelian')
plt.xlabel('Rating Produk')
plt.ylabel('Frekuensi Pembelian')
st.pyplot(fig)

# Statistik deskriptif untuk data yang telah dibersihkan
st.subheader('Statistik Deskriptif Data')
st.dataframe(df_cleaned.describe())

# Dropdown untuk memilih kategori produk
category_option = st.selectbox(
    'Pilih Kategori Produk',
    df_cleaned['product_category_name'].unique()
)

# Menampilkan data berdasarkan kategori produk yang dipilih
filtered_data = df_cleaned[df_cleaned['product_category_name'] == category_option]
st.write(f"Menampilkan data untuk kategori: {category_option}")
st.dataframe(filtered_data.head())

# Filter rating produk
min_rating = st.slider(
    'Pilih Rating Minimum Produk',
    min_value=1,
    max_value=5,
    value=3
)

# Menampilkan produk dengan rating >= rating minimum
filtered_by_rating = df_cleaned[df_cleaned['review_score'] >= min_rating]
st.write(f"Menampilkan produk dengan rating >= {min_rating}")
st.dataframe(filtered_by_rating.head())

# Tombol untuk mengunduh data
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(filtered_by_rating)
st.download_button(
    label="Download Data sebagai CSV",
    data=csv,
    file_name='filtered_data.csv',
    mime='text/csv',
)