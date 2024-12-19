import streamlit as st

# Fungsi menghitung harga setelah diskon
def fungsi_diskon(harga_per_5menit, durasi):
    if durasi >= 40:
        d = 0.7
    elif durasi >= 30:
        d = 0.8
    elif durasi >= 20:
        d = 0.9
    else:
        d = 1.0
    return harga_per_5menit * (durasi // 5) * d

# Inisialisasi
st.title("Aplikasi Kursi Pijat Elektronik")

# State pesanan
if "pesanan" not in st.session_state:
    st.session_state["pesanan"] = []
if "total_harga" not in st.session_state:
    st.session_state["total_harga"] = 0

# Daftar fitur pijat
fitur_options = {
    "Pijat Kepala": 5000,
    "Pijat Kaki": 6000,
    "Pijat Tangan": 7000,
    "Pijat Punggung": 8000
}

# Menambah pesanan
st.subheader("Tambah Pesanan")
fitur = st.selectbox("Pilih Fitur Pijat:", options=list(fitur_options.keys()))
kekuatan = st.slider("Pilih Kekuatan Pijat (1-5):", 1, 5, 3)
durasi = st.number_input("Masukkan Durasi (5, 10, 15 menit dan kelipatannya):", min_value=5, step=5)

if st.button("Tambah Pesanan"):
    if durasi % 5 == 0:
        harga_per_5menit = fitur_options[fitur]
        harga_diskon = fungsi_diskon(harga_per_5menit, durasi)
        st.session_state["pesanan"].append((fitur, durasi, kekuatan, harga_diskon))
        st.session_state["total_harga"] += harga_diskon
        st.success(f"Pesanan {fitur} berhasil ditambahkan!")
    else:
        st.error("Durasi harus kelipatan 5 menit!")

# Menampilkan daftar pesanan sementara
st.subheader("Pesanan yang Sudah Dilakukan:")
if st.session_state["pesanan"]:
    for idx, (fitur, durasi, kekuatan, harga) in enumerate(st.session_state["pesanan"]):
        st.write(f"{idx + 1}. {fitur} | Durasi: {durasi} menit | Kekuatan: {kekuatan} | Harga Setelah Diskon: Rp{harga:,.2f}")
    st.write(f"**Total Harga Sementara: Rp{st.session_state['total_harga']:,.2f}**")
else:
    st.write("Belum ada pesanan.")

# Konfirmasi pesanan akhir
if st.session_state["pesanan"]:
    st.subheader("Apakah ingin menambahkan pesanan lain?")
    tambah_lagi = st.radio("Pilih (Yes/No):", ["Yes", "No"], horizontal=True)
    if tambah_lagi == "No":
        st.subheader("Total Harga yang Harus Dibayar:")
        st.write(f"**Rp{st.session_state['total_harga']:,.2f}**")
        
        # Metode pembayaran
        st.subheader("Pilih Metode Pembayaran")
        metode = st.radio("Metode Pembayaran:", ["Cash", "QRIS"])
        if metode == "Cash":
            uang = st.number_input("Masukkan Jumlah Uang:", min_value=0)
            if st.button("Bayar"):
                if uang >= st.session_state["total_harga"]:
                    kembalian = uang - st.session_state["total_harga"]
                    st.success(f"Pembayaran berhasil! Kembalian Anda: Rp{kembalian:,.2f}")
                    st.session_state.clear()
                else:
                    st.error("Uang tidak cukup!")
        elif metode == "QRIS":
            password = st.text_input("Masukkan Password QRIS:", type="password")
            if st.button("Bayar"):
                if password == "1234":
                    st.success("Pembayaran berhasil melalui QRIS. Terima kasih!")
                    st.session_state.clear()
                else:
                    st.error("Password salah!")
