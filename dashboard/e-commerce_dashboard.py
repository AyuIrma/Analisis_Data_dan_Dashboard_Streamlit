import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi tampilan
sns.set(style="dark") 
st.set_page_config(layout="wide", page_title="E-Commerce Analysis Dashboard")

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    try:
        df_customers = pd.read_csv('../data/customers_dataset.csv')
        df_geolocation = pd.read_csv('../data/geolocation_dataset.csv')
        df_order_items = pd.read_csv('../data/order_items_dataset.csv')
        df_order_payments = pd.read_csv('../data/order_payments_dataset.csv')
        df_order_reviews = pd.read_csv('../data/order_reviews_dataset.csv')
        df_orders = pd.read_csv('../data/orders_dataset.csv')
        df_products = pd.read_csv('../data/products_dataset.csv')
        df_sellers = pd.read_csv('../data/sellers_dataset.csv')
        df_category_translation = pd.read_csv('../data/product_category_name_translation.csv')
        
        return df_customers, df_geolocation, df_order_items, df_order_payments, df_order_reviews, df_orders, df_products, df_sellers, df_category_translation
    except FileNotFoundError:
        st.error('File CSV tidak ditemukan. Pastikan path file sudah benar.')
        st.stop()

# Memuat data
df_customers, df_geolocation, df_order_items, df_order_payments, df_order_reviews, df_orders, df_products, df_sellers, df_category_translation = load_data()

# Judul dan Deskripsi
st.title('🛍️ E-Commerce Data Analysis Dashboard')
st.markdown('''
    ### Oleh: Ayu Irmawati
    Dashboard ini menampilkan analisis dari dataset e-commerce yang berfokus pada:
    1. Kategori produk yang paling sering dibeli
    2. Hubungan antara rating produk dan frekuensi pembelian
''')

# Data Cleaning
def clean_data():
    # Menggabungkan dataset dan membersihkan data
    df_cleaned = df_order_items.drop_duplicates()
    df_cleaned = pd.merge(df_cleaned, df_products[['product_id', 'product_category_name']], 
                         on='product_id', how='left')
    df_cleaned = df_cleaned.dropna(subset=['product_id', 'product_category_name'])
    
    # Menggabungkan dengan data review
    df_cleaned = pd.merge(df_cleaned, df_order_reviews[['order_id', 'review_score']], 
                         on='order_id', how='left')
    df_cleaned = df_cleaned.dropna(subset=['review_score'])
    
    return df_cleaned

df_cleaned = clean_data()

# Tab untuk berbagai analisis
tab1, tab2, tab3 = st.tabs(["📊 Analisis Kategori Produk", "⭐ Analisis Rating", "📈 Analisis Hubungan"])

with tab1:
    st.header("Analisis Kategori Produk Terlaris")
    
    # Menghitung dan menampilkan top 10 kategori
    category_counts = df_cleaned['product_category_name'].value_counts().head(10)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=category_counts.values, y=category_counts.index)
    plt.title('10 Kategori Produk Terlaris')
    plt.xlabel('Jumlah Pembelian')
    plt.ylabel('Kategori Produk')
    st.pyplot(fig)
    
    # Menampilkan data dalam tabel
    st.write("Detail 10 Kategori Teratas:")
    st.dataframe(category_counts.reset_index().rename(
        columns={'index': 'Kategori', 'product_category_name': 'Jumlah Pembelian'}))

with tab2:
    st.header("Analisis Rating Produk")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribusi rating
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data=df_cleaned, x='review_score', bins=5, kde=True)
        plt.title('Distribusi Rating Produk')
        plt.xlabel('Rating')
        plt.ylabel('Frekuensi')
        st.pyplot(fig)
        
    with col2:
        # Statistik rating
        st.write("Statistik Rating Produk:")
        st.dataframe(df_cleaned['review_score'].describe())

with tab3:
    st.header("Hubungan Rating dan Frekuensi Pembelian")
    
    # Menghitung metrics
    product_metrics = df_cleaned.groupby('product_id').agg({
        'order_id': 'count',
        'review_score': ['mean', 'sum']
    }).reset_index()
    product_metrics.columns = ['product_id', 'frequency', 'avg_rating', 'total_rating']
    
    # Visualisasi scatter plot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=product_metrics, x='avg_rating', y='frequency', alpha=0.5)
    plt.title('Hubungan antara Rating Produk dan Frekuensi Pembelian')
    plt.xlabel('Rata-rata Rating')
    plt.ylabel('Frekuensi Pembelian')
    st.pyplot(fig)
    
    # Correlation analysis
    correlation = product_metrics['avg_rating'].corr(product_metrics['frequency'])
    st.write(f"Korelasi antara rating dan frekuensi pembelian: {correlation:.2f}")

# Sidebar untuk filter
st.sidebar.header("Filter Data")

# Filter kategori
categories = ['Semua'] + list(df_cleaned['product_category_name'].unique())
selected_category = st.sidebar.selectbox('Pilih Kategori Produk', categories)

# Filter rating
min_rating = st.sidebar.slider('Rating Minimum', 1, 5, 1)

# Terapkan filter
filtered_data = df_cleaned.copy()
if selected_category != 'Semua':
    filtered_data = filtered_data[filtered_data['product_category_name'] == selected_category]
filtered_data = filtered_data[filtered_data['review_score'] >= min_rating]

# Tampilkan data terfilter
st.subheader('Data Terfilter')
st.write(f"Menampilkan {len(filtered_data)} data yang sesuai filter")
st.dataframe(filtered_data.head())

# Download data
st.sidebar.markdown("---")
csv = filtered_data.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="📥 Download Data Terfilter",
    data=csv,
    file_name='filtered_ecommerce_data.csv',
    mime='text/csv',
)

# Kesimpulan
st.markdown("""
---
### 📝 Kesimpulan:
1. **Kategori Produk Terlaris:**
   - Kategori cama_mesa_banho adalah yang paling sering dibeli
   - Menunjukkan preferensi kuat pelanggan terhadap produk dalam kategori ini

2. **Analisis Rating:**
   - Sebagian besar produk mendapat rating yang baik (4-5)
   - Distribusi rating menunjukkan kepuasan pelanggan yang tinggi

3. **Hubungan Rating dan Pembelian:**
   - Terdapat hubungan positif antara rating produk dan frekuensi pembelian
   - Produk dengan rating tinggi cenderung lebih sering dibeli
""")
