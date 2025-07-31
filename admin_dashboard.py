import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prediksi_siswa import get_all_nilai, get_all_predictions, get_all_users, insert_user, update_user, delete_user

# ====================
# Tambahkan CSS Custom
# ====================
def add_background_and_style():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }

        .stApp {
            background: linear-gradient(to right, #2b5876, #4e4376);
            background-size: cover;
            color: white;
        }

        h1, h2, h3, h4 {
            color: white;
        }

        .stTextInput input, .stPasswordInput input, .stSelectbox div, .stDataFrame, .stForm {
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

        .stTabs [role="tab"] {
            background-color: #444;
            color: white;
            border-radius: 8px;
        }

        .stTabs [aria-selected="true"] {
            background-color: #4CAF50;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

def admin_page():
    add_background_and_style()  # Tambahkan styling

    st.sidebar.title("Menu Admin")
    menu_admin = st.sidebar.radio("Pilih menu", [
        "Data Nilai Siswa", 
        "Hasil Prediksi Siswa", 
        "Manajemen Pengguna"
    ])

    if menu_admin == "Data Nilai Siswa":
        st.header("Data Nilai Siswa")
        data_nilai = get_all_nilai()
        df_nilai = pd.DataFrame(data_nilai, columns=["id", "Nama", "BIO", "KIMIA", "FIS", "MAT_L", "PKWU", "INF", "EKO", "GEO", "SOS", "Tanggal"])
        st.dataframe(df_nilai)

    elif menu_admin == "Hasil Prediksi Siswa":
        st.header("Hasil Prediksi Siswa")
        data_prediksi = get_all_predictions()
        df_prediksi = pd.DataFrame(data_prediksi, columns=["id", "Nama", "Hasil", "Tanggal"])
        st.dataframe(df_prediksi)

        st.subheader("Visualisasi Prediksi (Bar Chart)")
        fig_bar, ax_bar = plt.subplots()
        sns.countplot(data=df_prediksi, x="Hasil", palette="pastel", ax=ax_bar)
        plt.xticks(rotation=30, ha='right')
        st.pyplot(fig_bar)

        st.subheader("Tren Prediksi dari Waktu ke Waktu (Line Chart)")
        df_line = df_prediksi.groupby(["Tanggal", "Hasil"]).size().unstack(fill_value=0)
        st.line_chart(df_line)

        st.subheader("Distribusi Total Paket Peminatan (Pie Chart)")
        paket_counts = df_prediksi["Hasil"].value_counts()
        fig_pie, ax_pie = plt.subplots()
        ax_pie.pie(paket_counts, labels=paket_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
        ax_pie.axis('equal')
        st.pyplot(fig_pie)

    elif menu_admin == "Manajemen Pengguna":
        st.header("Manajemen Pengguna")
        users = get_all_users()
        df_users = pd.DataFrame(users, columns=["id", "Username", "Password", "Role"])
        st.dataframe(df_users)

        tab1, tab2 = st.tabs(["Tambah User", "Edit User"])

        with tab1:
            st.subheader("Tambah User")
            with st.form("tambah_user_form"):
                username_new = st.text_input("Username")
                password_new = st.text_input("Password")
                role_new = st.selectbox("Role", ["siswa", "admin"])
                submit_add = st.form_submit_button("Tambah")
                if submit_add:
                    insert_user(username_new, password_new, role_new)
                    st.success("User ditambahkan")

        with tab2:
            st.subheader("Edit User")
            with st.form("edit_user_form"):
                user_id = st.text_input("ID User")
                username = st.text_input("Username Baru")
                password = st.text_input("Password Baru")
                role = st.selectbox("Role Baru", ["siswa", "admin"])
                submit_edit = st.form_submit_button("Perbarui")
                if submit_edit:
                    update_user(user_id, username, password, role)
                    st.success("User diperbarui")

        st.subheader("Hapus User")
        user_id_delete = st.text_input("ID User yang akan dihapus")
        if st.button("Hapus User"):
            delete_user(user_id_delete)
            st.success("User dihapus")
