import streamlit as st
from admin_dashboard import admin_page
from user_dashboard import user_page
from prediksi_siswa import login

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

        h1 {
            text-align: center;
            color: white;
            font-size: 2.2em;
            font-weight: bold;
        }

        .stTextInput input, .stPasswordInput input, .stSelectbox div {
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

        </style>
    """, unsafe_allow_html=True)

# ====================
# Halaman Login
# ====================
def login_page():
    add_background_and_style()  # Tambahkan styling

    st.markdown("<h1>SELAMAT DATANG DI SISTEM<br>PREDIKSI PEMINATAN SISWA SMA</h1>", unsafe_allow_html=True)
    st.write("")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Login sebagai", ["user", "admin"])

    if st.button("Login"):
        user = login(username, password, role)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role
            st.success(f"Login berhasil sebagai {role}")
        else:
            st.error("Login gagal, periksa kembali username atau password")

# ====================
# Main App
# ====================
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_page()
    else:
        st.sidebar.write(f"Login sebagai: {st.session_state.role}")
        if st.session_state.role == "admin":
            admin_page()
        elif st.session_state.role == "user":
            user_page()

        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
