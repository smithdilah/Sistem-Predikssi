import mysql.connector
from datetime import datetime
import pandas as pd

# -------------------- KONEKSI DATABASE --------------------
def get_connection():
    return mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        user="sql12791207",                    # Username database kamu
        password="hiWy3TmaBM",          # Ganti dengan password kamu
        database="sql12791207",                # Nama database kamu
        port=3306
    )

# -------------------- LOGIN --------------------
def login(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s AND role=%s", (username, password, role))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

# -------------------- NILAI SISWA --------------------
def insert_nilai_siswa(nama, bio, kimia, fis, mat_l, pkwu, inf, eko, geo, sos):
    conn = get_connection()
    cursor = conn.cursor()
    tanggal = datetime.today().strftime('%Y-%m-%d')
    query = """
        INSERT INTO nilai_siswa 
        (nama, BIO, KIMIA, FIS, MAT_L, PKWU, INF, EKO, GEO, SOS, tanggal)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (nama, bio, kimia, fis, mat_l, pkwu, inf, eko, geo, sos, tanggal))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_nilai():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# -------------------- PREDIKSI --------------------
def insert_prediction(nama, hasil):
    conn = get_connection()
    cursor = conn.cursor()
    tanggal = datetime.today().strftime('%Y-%m-%d')
    cursor.execute("INSERT INTO hasil_prediksi (nama, hasil, tanggal) VALUES (%s, %s, %s)", (nama, hasil, tanggal))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_predictions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hasil_prediksi")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_training_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT ns.BIO, ns.KIMIA, ns.FIS, ns.MAT_L, ns.PKWU, ns.INF, ns.EKO, ns.GEO, ns.SOS, hp.nama
        FROM nilai_siswa ns
        JOIN hasil_prediksi hp ON ns.nama = hp.nama
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    df = pd.DataFrame(data)

    def tentukan_paket(row):
        skor_paket1 = row["MAT_L"] + row["FIS"] + row["KIMIA"] + row["BIO"] + row["PKWU"]
        skor_paket2 = row["GEO"] + row["EKO"] + row["KIMIA"] + row["INF"] + row["PKWU"]
        skor_paket3 = row["GEO"] + row["EKO"] + row["SOS"] + row["PKWU"]

        max_skor = max(skor_paket1, skor_paket2, skor_paket3)
        if max_skor == skor_paket1:
            return "Paket 1"
        elif max_skor == skor_paket2:
            return "Paket 2"
        else:
            return "Paket 3"

    df["hasil"] = df.apply(tentukan_paket, axis=1)
    X = df[["BIO", "KIMIA", "FIS", "MAT_L", "PKWU", "INF", "EKO", "GEO", "SOS"]]
    y = df["hasil"]
    return X, y

# -------------------- USER MANAGEMENT --------------------
def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def insert_user(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
    conn.commit()
    cursor.close()
    conn.close()

def update_user(user_id, username, password, role):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET username=%s, password=%s, role=%s WHERE id=%s", (username, password, role, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
