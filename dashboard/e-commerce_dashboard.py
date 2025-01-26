import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi tampilan plot
plt.style.use('seaborn')
st.set_page_config(layout="wide")

# Memuat dataset yang telah dibersihkan dan diproses
try:
    df_order_items = pd.read_csv('../data/order_items_dataset.csv')
    df_order_reviews = pd.read_csv('../data/order_reviews_dataset.csv')
    df_products = pd.read_csv('../data/products_dataset.csv')
except FileNotFoundError:
    st.error('File CSV tidak ditemukan. Pastikan path file sudah benar.')
    st.stop()

# Gabungkan dataset untuk analisis lebih lanjut
df_cleaned = pd.merge(df_order_items, df_products[['product_id', 'product_category_name']], on='product_id', how='left')
df_cleaned = pd.merge(df_cleaned, df_order_reviews[['order_id', 'review_score']], on='order_id', how='left')
df_cleaned = df_cleaned.dropna(subset=['review_score'])

# Menambahkan judul dan deskripsi dashboard
st.title('🛍️ E-Commerce Data Analysis Dashboard')
st.markdown('''
    ### Analisis Data E-Commerce
    Dashboard ini menampilkan analisis komprehensif dari dataset e-commerce, 
    berfokus pada pola pembelian produk dan penilaian pelanggan.
''')

# Analisis kategori produk yang paling sering dibeli
category_counts = df_cleaned['product_category_name'].value_counts().head(10)  # Top 10 kategori

# Membuat grafik bar untuk kategori produk yang paling sering dibeli
st.subheader('📊 Top 10 Kategori Produk Terlaris')
fig, ax = plt.subplots(figsize=(12, 6))
category_counts.plot(kind='bar', ax=ax)
plt.title('10 Kategori Produk Terlaris')
plt.xlabel('Kategori Produk')
plt.ylabel('Jumlah Pembelian')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig)

# Analisis rating dan frekuensi
st.subheader('📈 Analisis Rating dan Frekuensi Pembelian')

# Menghitung metrik
product_metrics = df_cleaned.groupby('product_id').agg({
    'order_id': 'count',  # frekuensi pembelian
    'review_score': ['mean', 'sum', 'count']  # rata-rata rating, total rating, jumlah review
}).reset_index()

product_metrics.columns = ['product_id', 'purchase_frequency', 'avg_rating', 'total_rating', 'review_count']

# Membuat visualisasi side by side
col1, col2 = st.columns(2)

with col1:
    st.write("#### Rata-rata Rating vs Frekuensi Pembelian")
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=product_metrics, x='avg_rating', y='purchase_frequency', alpha=0.5)
    plt.title('Hubungan Rata-rata Rating dengan Frekuensi Pembelian')
    plt.xlabel('Rata-rata Rating')
    plt.ylabel('Frekuensi Pembelian')
    st.pyplot(fig1)

with col2:
    st.write("#### Total Rating vs Frekuensi Pembelian")
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=product_metrics, x='total_rating', y='purchase_frequency', alpha=0.5)
    plt.title('Hubungan Total Rating dengan Frekuensi Pembelian')
    plt.xlabel('Total Rating')
    plt.ylabel('Frekuensi Pembelian')
    st.pyplot(fig2)

# Tampilkan statistik ringkasan
st.subheader('📊 Statistik Ringkasan')
col3, col4 = st.columns(2)

with col3:
    st.write("#### Statistik Rating Produk")
    st.dataframe(product_metrics.describe())

with col4:
    st.write("#### Top 5 Produk dengan Rating Tertinggi")
    top_products = product_metrics[product_metrics['review_count'] >= 10].nlargest(5, 'avg_rating')
    st.dataframe(top_products[['product_id', 'avg_rating', 'review_count']])

# Filter dan Interaksi
st.subheader('🔍 Filter Data')

# Dropdown untuk kategori
category_option = st.selectbox(
    'Pilih Kategori Produk',
    ['Semua'] + list(df_cleaned['product_category_name'].unique())
)

# Slider untuk rating
min_rating = st.slider(
    'Pilih Rating Minimum',
    min_value=1,
    max_value=5,
    value=3
)

# Terapkan filter
filtered_data = df_cleaned.copy()
if category_option != 'Semua':
    filtered_data = filtered_data[filtered_data['product_category_name'] == category_option]
filtered_data = filtered_data[filtered_data['review_score'] >= min_rating]

# Tampilkan hasil filter
st.write(f"Menampilkan {len(filtered_data)} data yang sesuai filter")
st.dataframe(filtered_data.head())

# Download data
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(filtered_data)
st.download_button(
    label="📥 Download Data Terfilter (CSV)",
    data=csv,
    file_name='filtered_ecommerce_data.csv',
    mime='text/csv',
)

# Menambahkan footer
st.markdown("""
---
### 📝 Catatan:
* Data diambil dari dataset e-commerce Brazil
* Rating produk berkisar dari 1 hingga 5
* Analisis mencakup frekuensi pembelian dan rating produk
""")
