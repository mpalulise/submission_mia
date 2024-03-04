import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from streamlit_option_menu import option_menu

all_df = pd.read_csv("https://raw.githubusercontent.com/mpalulise/Analisis-E-commerce/main/all_data.csv")

st.header('Dasbor Brazilian E-Commerce :sparkles:')

with st.sidebar:
    selected = option_menu(
        menu_title="DASHBOARD",
        options=["Insight Perkembangan Pemasukkan","Daftar Kota Teratas", "Metode Pembayaran Paling Umum"],
    )

if selected == "Insight Perkembangan Pemasukkan":
    st.subheader("Bagaimana Perkembangan Pemasukkan dari 2017 sampai 2018?")
    all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])
    monthly_orders_df = all_df.resample(rule='M', on='order_purchase_timestamp').agg({
    "order_id": "nunique",
    "payment_value": "sum"
    })
    monthly_orders_df.index = monthly_orders_df.index.strftime('%Y-%m')
    monthly_orders_df = monthly_orders_df.reset_index()
    monthly_orders_df.rename(columns={
    "order_id": "order_count",
    "payment_value": "revenue"
    }, inplace=True)

    fig = plt.figure(figsize=(10, 5))
    plt.plot(monthly_orders_df["order_purchase_timestamp"], monthly_orders_df["order_count"], marker='o', linewidth=2, color="lightcoral")
    plt.title("Jumlah Pembelian Tiap Bulan", loc="center", fontsize=15, fontname='Times New Roman', fontweight='bold')
    plt.xticks(rotation = 45, fontsize=10, fontname='Times New Roman')
    plt.yticks(fontsize=10,fontname='Times New Roman')
    plt.tight_layout()
    st.pyplot(fig)
    st.write("Diagram garis di atas menunjukkan bahwa jumlah pemasukkan dari Januari 2017 sampai Agustus 2018 cenderung stabil meningkat. Terlihat sekali perkembangannya dari awal yang masih sedikit, pelan-pelan merangkak sampai pemasukkannya tinggi! Dapat diketahui pula pada November 2017 memiliki jumlah pemasukkan terbesar, yaitu $1,162,150.28. Wow!")

if selected == "Daftar Kota Teratas":
    # Select the top 10 cities with the highest payment value
    city_payment = all_df.groupby('customer_city')['payment_value'].sum()
    city_payment = city_payment.sort_values(ascending=False)
    city_payment = pd.DataFrame(city_payment).reset_index()
    top_10_cities = city_payment.head(10)
    st.subheader("Kota Mana Saja yang Banyak Memberikan Pemasukkan?")

    fig = plt.figure(figsize=(10, 5))
    plt.bar(top_10_cities['customer_city'], top_10_cities['payment_value'], color='steelblue')
    plt.title('10 Kota Teratas Berdasarkan Jumlah Pemasukkan E-Commerce', fontsize=16, fontname='Times New Roman', fontweight='bold')
    plt.xlabel('Kota', fontsize=14, fontname='Times New Roman')
    plt.ylabel('Total nilai pemasukkan', fontsize=14, fontname='Times New Roman')
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    st.pyplot(fig)
    st.write("Dari sini terlihat bahwa Sao Paulo sebagai kota terbanyak memberikan pemasukkan ke Brazil E-commerce dengan total $2,121,162.32!")
    st.write("Hal ini wajar karena Sao Paulo merupakan salah satu kota cosmopolitan dan melting pot point di Brazil. Lalu diikuti dengan Rio de Janeiro dengan total pemasukkan sebesar $1,133,064.81!")
    st.write("Terlihat juga kalau Brasilia selaku ibukota Brazil berada di urutan keempat dengan total $348,311.16. Hm, kira-kira mengapa ya ibukota Brazil tidak menjadi kota terbanyak yang memberi pemasukkan ke Brazil E-Commerce?")

if selected == "Metode Pembayaran Paling Umum":
    st.subheader("Melalui Cara Pembayaran Apa yang Digunakan Pembeli di Beberapa Kota Teratas Pemberi Pemasukkan ke Brazil E-Commerce?")
    Five_cities = all_df[all_df['customer_city'].isin(['sao paulo', 'rio de janeiro','belo horizonte','brasilia','curitiba'])]
    five_cities = Five_cities[['customer_city','payment_type']]
    fig = plt.figure(figsize=(10, 6))
    sns.countplot(data=five_cities, x='customer_city', hue='payment_type', palette='viridis')
    plt.title('Cara Pembayaran Lima Kota Teratas', fontsize=16, fontname = 'Times New Roman', fontweight='bold')
    plt.xlabel('Kota', fontsize=14, fontname = 'Times New Roman')
    plt.ylabel('Cara Pembayaran', fontsize=14, fontname = 'Times New Roman')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(title='Payment Type', fontsize=12)
    plt.tight_layout()
    st.pyplot(fig)
    st.write("Dari grafik bar di atas, jelas bahwa credit_card atau kartu kredit dipilih banyak pembeli untuk melakukan pembayaran! Ini mungkin bisa menjadi peluang besar untuk memperoleh keuntungan lebih tinggi dengan bekerja sama dengan pihak-pihak perusahaan kartu kredit. Pilihan kedua jatuh kepada cara pembayaran dengan boleto.")
