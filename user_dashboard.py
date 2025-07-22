import streamlit as st
import pandas as pd
import joblib
from prediksi_siswa import insert_nilai_siswa, insert_prediction

# ============================
# Tambahkan Styling (CSS)
# ============================
def add_user_style():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(to right, #2b5876, #4e4376);
            color: white;
        }

        h1, h2, h3, h4 {
            color: white;
        }

        .stTextInput input, .stNumberInput input, .stSelectbox div {
            background-color: #333 !important;
            color: white !important;
            border-radius: 8px;
        }

        .stButton > button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border: none;
            padding: 0.5em 1em;
            border-radius: 8px;
        }

        .stButton > button:hover {
            background-color: #45a049;
        }

        .stAlert {
            background-color: rgba(255, 255, 255, 0.1);
        }

        .stDataFrame, .stTable {
            background-color: #222;
            color: white;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

# ============================
# Fungsi konversi nilai
# ============================
def nilai_ke_predikat(nilai):
    if nilai >= 85:
        return 'A'
    elif nilai >= 75:
        return 'B'
    elif nilai >= 65:
        return 'C'
    else:
        return 'D'

# ============================
# Halaman User
# ============================
def user_page():
    add_user_style()
    st.header("Input Nilai Siswa")

    nama = st.text_input("Nama")

    col1, col2, col3 = st.columns(3)
    with col1:
        bio = st.number_input("Biologi", 0.0, 100.0, format="%.2f")
        kimia = st.number_input("Kimia", 0.0, 100.0, format="%.2f")
        fis = st.number_input("Fisika", 0.0, 100.0, format="%.2f")
        mat_l = st.number_input("Matematika", 0.0, 100.0, format="%.2f")
    with col2:
        pkwu = st.number_input("PKWU", 0.0, 100.0, format="%.2f")
        inf = st.number_input("Informatika", 0.0, 100.0, format="%.2f")
    with col3:
        eko = st.number_input("Ekonomi", 0.0, 100.0, format="%.2f")
        geo = st.number_input("Geografi", 0.0, 100.0, format="%.2f")
        sos = st.number_input("Sosiologi", 0.0, 100.0, format="%.2f")

    if st.button("Simpan Nilai"):
        if not nama:
            st.error("Nama siswa harus diisi sebelum menyimpan nilai.")
        else:
            insert_nilai_siswa(nama, bio, kimia, fis, mat_l, pkwu, inf, eko, geo, sos)
            st.success("Nilai berhasil disimpan.")

    if st.button("Prediksi Peminatan"):
        if not nama:
            st.error("Nama siswa harus diisi.")
            return

        nilai_list = [bio, kimia, fis, mat_l, pkwu, inf, eko, geo, sos]

        if all(n == 0.0 for n in nilai_list):
            st.error("Semua nilai tidak boleh nol. Mohon isi minimal satu nilai dengan benar.")
            return

        if all(n == nilai_list[0] for n in nilai_list):
            st.error("Semua nilai tidak boleh sama. Mohon isi nilai dengan variasi.")
            return

        data_predikat = {
            "BIO": nilai_ke_predikat(bio),
            "KIMIA": nilai_ke_predikat(kimia),
            "FIS": nilai_ke_predikat(fis),
            "MAT_L": nilai_ke_predikat(mat_l),
            "PKWU": nilai_ke_predikat(pkwu),
            "INF": nilai_ke_predikat(inf),
            "EKO": nilai_ke_predikat(eko),
            "GEO": nilai_ke_predikat(geo),
            "SOS": nilai_ke_predikat(sos),
        }

        df = pd.DataFrame([data_predikat])

        try:
            model = joblib.load("model_peminatan.pkl")
            encoder = joblib.load("encoder_fitur.pkl")
        except FileNotFoundError:
            st.error("Model atau encoder tidak ditemukan.")
            return

        try:
            df_encoded = encoder.transform(df)
        except Exception as e:
            st.error(f"Terjadi kesalahan saat transformasi data: {e}")
            st.write("Nama kolom input:", df.columns.tolist())
            st.write("Tipe data:", df.dtypes)
            st.write("Nilai input:", df)
            st.write("Fitur yang diharapkan encoder:", getattr(encoder, 'feature_names_in_', 'Tidak diketahui'))
            return

        try:
            hasil = model.predict(df_encoded)[0]
            hasil = str(hasil)  # ✅ konversi dari numpy.str_ ke string biasa
        except Exception as e:
            st.error(f"Terjadi kesalahan saat prediksi: {e}")
            return

        paket_mapping = {
            "Paket 1": "Paket 1: Matematika Lanjut, Fisika, Kimia, Biologi, PKWU",
            "Paket 2": "Paket 2: Geografi, Ekonomi, Kimia, Informatika, PKWU",
            "Paket 3": "Paket 3: Geografi, Ekonomi, Sosiologi, PKWU"
        }
        hasil_full = str(paket_mapping.get(hasil, hasil))  # ✅ pastikan string murni

        try:
            insert_prediction(nama, hasil_full)
            st.success(f"Hasil Prediksi Peminatan: {hasil_full}")
        except Exception as e:
            st.error(f"Prediksi berhasil, tapi gagal menyimpan ke database: {e}")
