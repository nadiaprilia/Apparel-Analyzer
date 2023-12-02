import streamlit as st
import pandas as pd
import os
from PIL import Image
import matplotlib.pyplot as plt
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# Judul Aplikasi Web
st.markdown('''
# :rainbow[**APPAREL ANALYZER**] **: Implementasi Market Basket Analysis untuk Produk Fashion**
---

**Credit:** App built in `Python` + `Streamlit` by [Kelompok 2 ATLAS Teams]

---
''')

image = Image.open('images/MBA.jpg')

st.image(image, caption='Gambar Ilustrasi Market Basket Analysis')

with st.sidebar.header('Upload your CSV data'):
    uploaded_files = st.file_uploader("Choose CSV file", type=["csv"])

st.markdown('''
Sistem Apparel Analyzer adalah sistem yang kami kembangkan untuk industri fashion dimana perusahaan akan menerapkan teknologi mutakhir untuk mengoptimalkan manajemen inventaris. 
Sistem ini memanfaatkan kecerdasan buatan (AI) dan analisis data yang canggih untuk mencapai efisiensi yang lebih besar dalam operasi kami.

Pastikan dataset yang diunggah mengandung kolom yang diperlukan, seperti 'transaction', 'Items', 'No transaksi', 'Jenis' dan 'Qty'; untuk hasil yang akurat.
''')

print(uploaded_files)  # Check the value before passing it to pd.read_csv()

# Membaca file CSV
# Assuming uploaded_files contains the file path
if uploaded_files is not None:
    data = pd.read_csv(uploaded_files)
    st.subheader("Tampilan Data Anda: ")
    st.write("Data from CSV file:")
    st.write(data)
    # Tampilkan nama-nama kolom menggunakan Streamlit
    st.subheader("Nama - Nama Kolom:")
    st.write(data.columns.tolist())  # Mengonversi nama kolom menjadi list

    # Tampilkan nilai unik dari satu kolom saja
    column_name = 'Jenis'  # Ganti 'nama_kolom' dengan nama kolom yang diinginkan
    unique_values = data[column_name].unique()

    st.subheader(f"Nilai unik di Kolom '{column_name}':")
    for value in unique_values:
        st.write(value) 

    # Assuming columns are named 'Product' and 'Quantity' (adjust accordingly)
    if 'Items' in data.columns and 'Qty' in data.columns:

        # Grouping by Product and summing the Quantity
        product_quantity = data.groupby('Items')['Qty'].sum()

        # Mengambil produk yang paling banyak diminati (misalnya, 10 produk teratas)
        top_products = product_quantity.sort_values(ascending=False).head(10)

        # Create a color palette based on the number of products
        colors = plt.cm.viridis(range(len(top_products)))

        # Menampilkan bar chart dengan Matplotlib
        st.subheader('Grafik Produk Paling Diminati')
        fig, ax = plt.subplots()
        bars = ax.bar(top_products.index, top_products.values, color=colors)
        plt.xticks(rotation=45)
        plt.xlabel('Items')
        plt.ylabel('Frekuensi')

         # Adding labels for product quantities
        for i, value in enumerate(top_products.values):
            ax.text(i, value + 1, str(value), ha='center', va='bottom')

        # Menampilkan bar
        st.pyplot(fig)
    else:
        st.write("Columns 'items' and 'Qty' not found in the uploaded file. Please check the column names.")
        
    st.subheader('Hasil Perhitungan Data Anda')
    # Memisahkan setiap item pada setiap transaksi
    transactions = [transaction.split(', ') for transaction in data['Items']]

    # If transactions are successfully defined
    if transactions:

        # Convert transactions to a one-hot encoded format
        te = TransactionEncoder()
        te_ary = te.fit(transactions).transform(transactions)
        oht = pd.DataFrame(te_ary, columns=te.columns_)
       
        # Perform market basket analysis steps...
        frequent_itemsets = apriori(oht, min_support=0.001, use_colnames=True)
        st.markdown('<p style="color: yellow;">Frequent Itemsets :</p>', unsafe_allow_html=True)
        st.markdown('''Frequent itemsets adalah himpunan item yang muncul bersama secara teratur dalam dataset transaksi atau dalam konteks market basket analysis. Dalam analisis keranjang belanja, frequent itemsets mengacu pada kombinasi item yang sering dibeli bersama-sama oleh pelanggan.''')
        st.write(frequent_itemsets)

        # Mengekstrak kolom yang diperlukan (misalnya, ID transaksi dan daftar item)
        # Gantilah 'TransactionID' dan 'Items' dengan kolom yang sesuai pada dataset Anda
        selected_columns = ['transaction', 'Items']
        df = data[selected_columns]
 
            # Transaksi pada jenis Pakaian Pria 
        basket_Pakaian_Pria = (data[data['Jenis'] =="Pakaian Pria"] 
                .groupby(['No transaksi', 'Items'])['Qty'] 
                .sum().unstack().reset_index().fillna(0) 
                .set_index('No transaksi')) 
  
            # Transaksi pada jenis Pakaian Wanita 
        basket_Pakaian_Wanita = (data[data['Jenis'] =="Pakaian Wanita"] 
                .groupby(['No transaksi', 'Items'])['Qty'] 
                .sum().unstack().reset_index().fillna(0) 
                .set_index('No transaksi')) 
  
            # Transaksi pada jenis Tas Wanita 
        basket_Tas_Wanita = (data[data['Jenis'] =="Tas Wanita"] 
                .groupby(['No transaksi', 'Items'])['Qty'] 
                .sum().unstack().reset_index().fillna(0) 
                .set_index('No transaksi'))  
  
            # Transaksi pada jenis Sepatu
        basket_Sepatu = (data[data['Jenis'] =="Sepatu"] 
                .groupby(['No transaksi', 'Items'])['Qty'] 
                .sum().unstack().reset_index().fillna(0) 
                .set_index('No transaksi'))
    
            # Transaksi pada jenis Jilbab 
        basket_Jilbab = (data[data['Jenis'] =="Jilbab"] 
                .groupby(['No transaksi', 'Items'])['Qty'] 
                .sum().unstack().reset_index().fillna(0) 
                .set_index('No transaksi'))
    
        # Transaksi pada jenis Celana Dalam Pria 
        basket_Celana_Dalam_Pria = (data[data['Jenis'] =="Celana Dalam Pria"] 
          .groupby(['No transaksi', 'Items'])['Qty'] 
          .sum().unstack().reset_index().fillna(0) 
          .set_index('No transaksi'))
    
        # Transaksi pada jenis Celana Dalam Wanita 
        basket_Celana_Dalam_Wanita = (data[data['Jenis'] =="Celana Dalam Wanita"] 
          .groupby(['No transaksi', 'Items'])['Qty'] 
          .sum().unstack().reset_index().fillna(0) 
          .set_index('No transaksi')) 
    
        # Transaksi pada jenis Tas Pria 
        basket_Tas_Pria = (data[data['Jenis'] =="Tas Pria"] 
          .groupby(['No transaksi', 'Items'])['Qty'] 
          .sum().unstack().reset_index().fillna(0) 
          .set_index('No transaksi'))
    
        # Transaksi pada jenis Jam Tangan 
        basket_Jam_Tangan = (data[data['Jenis'] =="Jam Tangan"] 
          .groupby(['No transaksi', 'Items'])['Qty'] 
          .sum().unstack().reset_index().fillna(0) 
          .set_index('No transaksi'))
        
        # Defining the hot encoding function to make the data suitable  
        # for the concerned libraries 
        def hot_encode(x): 
            if(x<= 0): 
                return 0
            if(x>= 1): 
                return 1
  
        # Encoding the datasets 
        basket_encoded = basket_Pakaian_Pria.applymap(hot_encode) 
        basket_Pakaian_Pria = basket_encoded 
  
        basket_encoded = basket_Pakaian_Wanita.applymap(hot_encode) 
        basket_Pakaian_Wanita = basket_encoded 
  
        basket_encoded = basket_Tas_Wanita.applymap(hot_encode) 
        basket_Tas_Wanita = basket_encoded  
  
        basket_encoded = basket_Sepatu.applymap(hot_encode) 
        basket_Sepatu = basket_encoded

        basket_encoded = basket_Jilbab.applymap(hot_encode) 
        basket_Jilbab = basket_encoded

        basket_encoded = basket_Celana_Dalam_Pria.applymap(hot_encode) 
        basket_Celana_Dalam_Pria = basket_encoded 

        basket_encoded = basket_Celana_Dalam_Wanita.applymap(hot_encode) 
        basket_Celana_Dalam_Wanita = basket_encoded

        basket_encoded = basket_Tas_Pria.applymap(hot_encode) 
        basket_Tas_Pria = basket_encoded 

        basket_encoded = basket_Jam_Tangan.applymap(hot_encode) 
        basket_Jam_Tangan = basket_encoded 

        st.markdown('<p style="color: yellow;">Model Association Rule :</p>', unsafe_allow_html=True)
        st.markdown('''Dalam Market Basket Analysis, Association Rules digunakan untuk mengungkapkan hubungan antara produk yang dibeli bersamaan. Contoh algoritma yang digunakan dalam model ini adalah algoritma Apriori, yang digunakan untuk menemukan aturan asosiasi di antara item-item dalam kumpulan data.''')
        # Building the model 
        frq_items = apriori(basket_Pakaian_Pria, min_support = 0.05, use_colnames = True) 
  
        # Collecting the inferred rules in a dataframe 
        rules = association_rules(frq_items, metric ="lift", min_threshold = 0.1) 
        rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False]) 
        st.write("Model Association Rule Berdasarkan Jenis Pakaian Pria :")
        st.write(rules.head())

        frq_items = apriori(basket_Pakaian_Wanita, min_support = 0.05, use_colnames = True) 
        rules = association_rules(frq_items, metric ="lift", min_threshold = 0.1) 
        rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False]) 
        st.write("Model Association Rule Berdasarkan Jenis Pakaian Wanita :")
        st.write(rules.head())

        frq_items = apriori(basket_Tas_Wanita, min_support = 0.05, use_colnames = True) 
        rules = association_rules(frq_items, metric ="lift", min_threshold = 0.1) 
        rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False]) 
        st.write("Model Association Rule Berdasarkan Jenis Tas Wanita :")
        st.write(rules.head())

        frq_items = apriori(basket_Sepatu, min_support = 0.05, use_colnames = True) 
        rules = association_rules(frq_items, metric ="lift", min_threshold = 0.1) 
        rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False]) 
        st.write("Model Association Rule Berdasarkan Jenis Sepatu :")
        st.write(rules.head())

        frq_items = apriori(basket_Jilbab, min_support = 0.05, use_colnames = True) 
        rules = association_rules(frq_items, metric ="lift", min_threshold = 0.1) 
        rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False]) 
        st.write("Model Association Rule Berdasarkan Jenis Jilbab :")
        st.write(rules.head())

        frq_items = apriori(basket_Jam_Tangan, min_support = 0.05, use_colnames = True) 
        rules = association_rules(frq_items, metric ="lift", min_threshold = 0.1) 
        rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False]) 
        st.write("Model Association Rule Berdasarkan Jenis Jam Tangan :")
        st.write(rules.head())

        def market_basket_analysis(data, min_support):
            # Preprocessing data
            basket = (data
                .groupby(['transaction', 'Items'])['Qty']
                .sum().unstack().reset_index().fillna(0)
                .set_index('transaction'))

                # Encoding data
            basket_sets = basket.applymap(lambda x: 1 if x > 0 else 0)

                #Apriori algorithm
            frequent_itemsets = apriori(basket_sets, min_support=min_support, use_colnames=True)

                # Association Rules
            rules = association_rules(frequent_itemsets, metric="lift", min_threshold=0.1)
    
                # Melakukan one-hot encoding pada kolom 'Items'
            oht = df['Items'].str.get_dummies(sep=',')  # Jika item dipisahkan oleh delimiter tertentu, ganti ',' dengan delimiter yang benar
            st.write("One-hot encoded DataFrame :")
            st.write(oht)

                # Menampilkan aturan asosiasi jika tidak kosong
            if rules.empty:
                st.write("Tidak ada aturan asosiasi yang ditemukan dengan nilai threshold yang diberikan.")
            else:
                st.write("Aturan Asosiasi:")
                st.write(rules)    
    else:
        st.write("No transaction data found.")
else:
    st.write("No file uploaded or invalid file.")


#susunan anggota kelompok
st.subheader("Apparel Analyzer Teams")

# Misalnya, path ke folder tempat gambar disimpan
folder_path = 'C:/Users/Lenovo/OneDrive/Documents/Apparel Analyzer/images'

def tampilkan_jejeran_gambar(gambar_paths, ukuran=720):
    # Bagi layar menjadi 5 bagian
    col1, col2, col3, col4, col5 = st.columns(5)

     # Tampilkan gambar di setiap kolom
    with col1:
        img1 = Image.open(gambar_paths[0])
        st.image(img1, width=ukuran, use_column_width=True)
        st.markdown(
            f'<p style="text-align:center; font-family:poppins;">Nadia</p>', 
            unsafe_allow_html=True)
        st.markdown(f'<style>div.stImage img {{width: {ukuran}px; height: {ukuran}px;}}</style>', unsafe_allow_html=True)

    with col2:
        img2 = Image.open(gambar_paths[1])
        st.image(img2, width=ukuran, use_column_width=True)
        st.markdown(
            f'<p style="text-align:center; font-family:poppins;">Fena</p>', 
            unsafe_allow_html=True)
        st.markdown(f'<style>div.stImage img {{width: {ukuran}px; height: {ukuran}px;}}</style>', unsafe_allow_html=True)

    with col3:
        img3 = Image.open(gambar_paths[2])
        st.image(img3, width=ukuran, use_column_width=True)
        st.markdown(
            f'<p style="text-align:center; font-family:poppins;">Yafi</p>', 
            unsafe_allow_html=True)
        st.markdown(f'<style>div.stImage img {{width: {ukuran}px; height: {ukuran}px;}}</style>', unsafe_allow_html=True)

    with col4:
        img4 = Image.open(gambar_paths[3])
        st.image(img4, width=ukuran, use_column_width=True)
        st.markdown(
            f'<p style="text-align:center; font-family:poppins;">Tohir</p>', 
            unsafe_allow_html=True)
        st.markdown(f'<style>div.stImage img {{width: {ukuran}px; height: {ukuran}px;}}</style>', unsafe_allow_html=True)

    with col5:
        img5 = Image.open(gambar_paths[4])
        st.image(img5, width=ukuran, use_column_width=True)
        st.markdown(
            f'<p style="text-align:center; font-family:poppins;">Hilda</p>', 
            unsafe_allow_html=True)
        st.markdown(f'<style>div.stImage img {{width: {ukuran}px; height: {ukuran}px;}}</style>', unsafe_allow_html=True)


# Daftar path gambar yang ingin ditampilkan
gambar_list = [
    'C:/Users/Lenovo/OneDrive/Documents/Apparel Analyzer/images/Nadia.jpg',
    'C:/Users/Lenovo/OneDrive/Documents/Apparel Analyzer/images/fena.jpg',
    'C:/Users/Lenovo/OneDrive/Documents/Apparel Analyzer/images/yafi.jpeg',
    'C:/Users/Lenovo/OneDrive/Documents/Apparel Analyzer/images/tohir.jpeg',
    'C:/Users/Lenovo/OneDrive/Documents/Apparel Analyzer/images/hilda.jpg'
]

# Panggil fungsi untuk menampilkan 5 gambar bersebelahan dengan ukuran yang sama
tampilkan_jejeran_gambar(gambar_list)