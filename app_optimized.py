import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Set Page Configuration
st.set_page_config(
    page_title="Prediksi Kelulusan Mahasiswa",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Clean UI CSS
st.markdown("""
<style>
    /* Main Theme Colors */
    :root {
        --primary: #6C63FF;
        --secondary: #00C89C;
        --background: #FAFAFA;
        --surface: #FFFFFF;
        --text: #333333;
        --light-text: #737373;
        --danger: #FF5555;
        --warning: #FFBE0B;
        --success: #00C897;
    }
    
    /* Overall Page Styling */
    .main {
        background-color: var(--background);
        color: var(--text);
        padding: 2rem 0;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Card Styling */
    .card {
        background-color: var(--surface);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
    }
    
    /* Header Styling */
    .header {
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        border-radius: 16px;
        color: white;
    }
    
    h1 {
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
    }
    
    /* Input Form Styling */
    .input-container {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1rem;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        color: white;
        border-radius: 50px;
        padding: 0.5rem 2rem;
        border: none;
        font-weight: 600;
        width: 100%;
        height: 3rem;
        transition: all 0.3s;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 1rem;
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, var(--secondary), var(--primary));
        box-shadow: 0 10px 20px rgba(108, 99, 255, 0.2);
    }
    
    /* Progress Bar Styling */
    .stProgress > div > div {
        background-image: linear-gradient(to right, var(--primary), var(--secondary));
        border-radius: 100px;
    }
    
    /* Result Box Styling */
    .result-container {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin-top: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }
    
    .result-tepat {
        color: var(--success);
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .result-terlambat {
        color: var(--danger);
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    /* Sidebar Customization */
    .css-1d391kg, .css-1v3fvcr {
        background-color: var(--surface) !important;
    }
    
    /* Table Styling */
    thead tr th {
        background-color: var(--primary) !important;
        color: white !important;
        text-align: center !important;
        font-weight: 600 !important;
    }
    
    tbody tr:nth-child(even) {
        background-color: #f8f9fa !important;
    }
    
    tbody tr:hover {
        background-color: #e9ecef !important;
    }
    
    th, td {
        padding: 12px 15px !important;
        font-size: 0.9rem !important;
    }
    
    /* Slider Customization */
    .stSlider > div > div > div {
        background-color: var(--primary) !important;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Footer Styling */
    .footer {
        text-align: center;
        padding-top: 2rem;
        color: var(--light-text);
        font-size: 0.8rem;
        border-top: 1px solid #eaeaea;
        margin-top: 3rem;
    }
    
    /* Icon Styling */
    .icon-large {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .card {
            padding: 1rem;
        }
        
        .header {
            padding: 1rem;
        }
    }
    
    /* Progress Label */
    .progress-label {
        margin-top: 5px;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    /* Charts Styling */
    .chart-container {
        background: white;
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }
    
    /* Prediction Info Box */
    .info-box {
        background-color: #e3f2fd;
        border-left: 5px solid var(--primary);
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
        font-size: 0.9rem;
    }
    
    /* Ensure emoji visibility */
    .emoji {
        font-family: "Segoe UI Emoji", "Noto Color Emoji", "Apple Color Emoji", sans-serif;
        font-size: 1.2em;
        display: inline-block;
    }
    
    /* Better visibility for sidebar */
    .css-hxt7ib {
        padding-top: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    /* Fix for Streamlit dataframe */
    .stDataFrame {
        width: 100% !important;
    }
    
    /* Fix for element containers */
    .element-container {
        margin-bottom: 10px !important;
    }
    
    /* Make dividers more visible */
    hr {
        border-color: #e9ecef;
        margin: 1rem 0;
    }
    
    /* Fix button hover states */
    button:focus {
        box-shadow: none !important;
    }
    
    /* Fix selectbox styling */
    div[data-baseweb="select"] {
        border-radius: 10px !important;
    }
    
    /* Tooltip styling */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 120px;
        background-color: black;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Fix header alignment in columns */
    .stColumn > div:first-child > div:first-child {
        margin-top: 0 !important;
    }
    
    /* Make card hover smoother */
    .card {
        will-change: transform;
        transform: translateZ(0);
        backface-visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Fungsi untuk mengonversi plot menjadi image
def get_img_with_href(fig, href):
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    return f'<a href="{href}" target="_blank"><img src="data:image/png;base64,{b64}" width="100%"></a>'

try:
    # Load trained model
    model_path = 'trained_model_xgboost.pkl'  # Changed model path to XGBoost model
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
except Exception as e:
    st.error(f"Error loading model: {str(e)}")
    model = None

# Layout dengan 3 kolom
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    # Header
    st.markdown("""
        <div class="header">
            <div class="icon-large">🎓</div>
            <h1>Prediksi Kelulusan Mahasiswa</h1>
            <p style='font-size:1.1rem;'>
                Sistem cerdas untuk memprediksi status kelulusan mahasiswa menggunakan algoritma <b>XGBoost</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

# Sidebar for user inputs
st.sidebar.markdown("""
    <div style="text-align: center; padding-bottom: 20px;">
        <h3><span style="display: inline-block;">📋</span> Input Data Mahasiswa</h3>
        <p style="font-size: 0.9rem;">Isi formulir berikut untuk mendapatkan prediksi kelulusan</p>
    </div>
""", unsafe_allow_html=True)

# Tambahkan latar belakang ke sidebar
st.sidebar.markdown("""
    <div class="card">
        <p style="text-align: center; font-weight: 600; margin-bottom: 15px;">Data Akademik & Pribadi</p>
    </div>
""", unsafe_allow_html=True)

def user_input_features():
    # Personal Information (Container bergaya card)
    st.sidebar.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.sidebar.markdown('<p style="font-weight: 600; color: #6C63FF; margin-bottom: 10px;"><span style="display: inline-block;">📌</span> Informasi Pribadi</p>', unsafe_allow_html=True)
    jenis_kelamin = st.sidebar.selectbox("Jenis Kelamin", ("LAKI-LAKI", "PEREMPUAN"))
    status_mahasiswa = st.sidebar.selectbox("Status Mahasiswa", ("TIDAK BEKERJA", "BEKERJA"))
    status_nikah = st.sidebar.selectbox("Status Nikah", ("BELUM MENIKAH", "MENIKAH"))
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Academic Information
    st.sidebar.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.sidebar.markdown('<p style="font-weight: 600; color: #6C63FF; margin-bottom: 10px;"><span style="display: inline-block;">📚</span> Nilai Akademik</p>', unsafe_allow_html=True)
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        ips1 = st.slider("IPS 1", 0.0, 4.0, 2.0, 0.01)
        ips3 = st.slider("IPS 3", 0.0, 4.0, 2.0, 0.01)
        ips5 = st.slider("IPS 5", 0.0, 4.0, 2.0, 0.01)
    with col2:
        ips2 = st.slider("IPS 2", 0.0, 4.0, 2.0, 0.01)
        ips4 = st.slider("IPS 4", 0.0, 4.0, 2.0, 0.01)
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    data = {
        'Jenis Kelamin': jenis_kelamin,
        'Status Mahasiswa': status_mahasiswa,
        'Status Nikah': status_nikah,
        'IPS 1': ips1,
        'IPS 2': ips2,
        'IPS 3': ips3,
        'IPS 4': ips4,
        'IPS 5': ips5
    }
    features = pd.DataFrame(data, index=[0])
    return features

# Get user inputs
input_df = user_input_features()

# Dashboard Main Area with two columns
col_main1, col_main2 = st.columns([2, 1])

with col_main1:
    # Display user input before encoding in a card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: #6C63FF; margin-bottom: 15px;"><span style="display: inline-block;">👤</span> Data Mahasiswa</h4>', unsafe_allow_html=True)
    st.dataframe(input_df, use_container_width=True)
    
    # Visualisasi IPS
    st.markdown('<h5 style="margin-top: 20px;"><span style="display: inline-block;">📊</span> Tren Nilai IPS</h5>', unsafe_allow_html=True)
    
    # Membuat chart untuk tren IPS
    ips_values = [input_df['IPS 1'].values[0], input_df['IPS 2'].values[0], 
                  input_df['IPS 3'].values[0], input_df['IPS 4'].values[0], 
                  input_df['IPS 5'].values[0]]
    semesters = ['Semester 1', 'Semester 2', 'Semester 3', 'Semester 4', 'Semester 5']
    
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(semesters, ips_values, marker='o', linewidth=2, color='#6C63FF')
    ax.set_ylim(0, 4.0)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_title('Tren Nilai IPS per Semester')
    
    # Hitung rata-rata IPS
    avg_ips = sum(ips_values) / len(ips_values)
    
    # Tampilkan garis rata-rata
    ax.axhline(y=avg_ips, color='#FF5555', linestyle='--', alpha=0.8)
    ax.text(0, avg_ips + 0.05, f'Rata-rata: {avg_ips:.2f}', color='#FF5555')
    
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with col_main2:
    # Encode user input
    input_df_encoded = input_df.copy()
    input_df_encoded['Jenis Kelamin'] = input_df_encoded['Jenis Kelamin'].map({'LAKI-LAKI': 0, 'PEREMPUAN': 1})
    input_df_encoded['Status Mahasiswa'] = input_df_encoded['Status Mahasiswa'].map({'TIDAK BEKERJA': 1, 'BEKERJA': 0})
    input_df_encoded['Status Nikah'] = input_df_encoded['Status Nikah'].map({'BELUM MENIKAH': 0, 'MENIKAH': 1})
    input_df_encoded.columns = ['JENIS KELAMIN', 'STATUS MAHASISWA', 'STATUS NIKAH', 'IPS 1', 'IPS 2', 'IPS 3', 'IPS 4', 'IPS 5']

    # Card untuk tombol prediksi
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: #6C63FF; text-align: center; margin-bottom: 15px;">Hasil Prediksi</h4>', unsafe_allow_html=True)
    
    # Prediction button
    if model is not None and st.button("✨ Prediksi Status Kelulusan"):
        try:
            prediction = model.predict(input_df_encoded)
            prediction_proba = model.predict_proba(input_df_encoded)

            kelulusan = "TEPAT WAKTU" if prediction[0] == 0 else "TERLAMBAT"
            
            # Convert float32 to Python float
            prob_tepat_waktu = float(prediction_proba[0][0])
            prob_terlambat = float(prediction_proba[0][1])

            # Hasil prediksi dengan animasi
            if kelulusan == "TEPAT WAKTU":
                st.balloons()  # Animasi balon untuk hasil positif
                st.markdown(f"""
                    <div style="text-align: center; margin: 20px 0;">
                        <div style="font-size: 64px; display: block; margin: 0 auto;">✅</div>
                        <div class="result-tepat">TEPAT WAKTU</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="text-align: center; margin: 20px 0;">
                        <div style="font-size: 64px; display: block; margin: 0 auto;">⏰</div>
                        <div class="result-terlambat">TERLAMBAT</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Gauge chart untuk probabilitas
            st.markdown("<p style='font-weight: 600; margin-top: 20px;'>Probabilitas Prediksi:</p>", unsafe_allow_html=True)
            
            col_prob1, col_prob2 = st.columns(2)
            
            with col_prob1:
                st.markdown(f"<p style='text-align: center; color: #00C897;'>Tepat Waktu</p>", unsafe_allow_html=True)
                st.progress(prob_tepat_waktu)
                st.markdown(f"<p class='progress-label' style='text-align: center; color: #00C897;'>{prob_tepat_waktu*100:.1f}%</p>", unsafe_allow_html=True)
                
            with col_prob2:
                st.markdown(f"<p style='text-align: center; color: #FF5555;'>Terlambat</p>", unsafe_allow_html=True)
                st.progress(prob_terlambat)
                st.markdown(f"<p class='progress-label' style='text-align: center; color: #FF5555;'>{prob_terlambat*100:.1f}%</p>", unsafe_allow_html=True)
            
            # Tambahkan faktor-faktor penting
            st.markdown("<p style='font-weight: 600; margin-top: 20px;'>Faktor Utama Prediksi:</p>", unsafe_allow_html=True)
            
            # Informasional tentang faktor penting (contoh sederhana)
            faktor = []
            if input_df['IPS 1'].values[0] < 2.0:
                faktor.append("⚠️ IPS 1 rendah")
            if input_df['IPS 5'].values[0] < 2.0:
                faktor.append("⚠️ IPS 5 rendah")
            if input_df['Status Mahasiswa'].values[0] == "BEKERJA":
                faktor.append("👨‍💼 Status bekerja")
            if input_df['Status Nikah'].values[0] == "MENIKAH":
                faktor.append("💍 Status menikah")
            
            # Jika tidak ada faktor spesifik yang terdeteksi
            if not faktor:
                if avg_ips < 2.5:
                    faktor.append("⚠️ Rata-rata IPS rendah")
                else:
                    faktor.append("📈 Performa akademik umum")
            
            # Tampilkan faktor
            for f in faktor:
                st.markdown(f"<div style='padding: 8px 0;'>{f}</div>", unsafe_allow_html=True)
            
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown("💡 <b>Catatan</b>: Prediksi ini berdasarkan model XGBoost yang telah dilatih. Hasil aktual dapat berbeda tergantung pada faktor lain.", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error during prediction: {str(e)}")
            
    else:
        # Tampilan default sebelum prediksi
        st.markdown("""
            <div style="text-align: center; padding: 30px 0;">
                <div style="font-size: 48px; color: #6C63FF; margin-bottom: 10px; display: block;">🔮</div>
                <p style="color: #737373;">Klik tombol di atas untuk mendapatkan hasil prediksi kelulusan</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Information cards
with col2:
    # Penjelasan Tentang XGBoost
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: #6C63FF; margin-bottom: 15px;"><span style="display: inline-block;">ℹ️</span> Tentang Model</h4>', unsafe_allow_html=True)
    st.markdown("""
        <p style="text-align: justify; font-size: 0.9rem;">
            Sistem ini menggunakan algoritma <b>XGBoost</b> (Extreme Gradient Boosting), 
            sebuah metode machine learning berbasis ensemble yang sangat efektif untuk 
            prediksi klasifikasi. Model ini dilatih dengan data historis mahasiswa dan mampu
            mengidentifikasi pola-pola yang berkaitan dengan kelulusan tepat waktu.
        </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Tips untuk mahasiswa
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: #6C63FF; margin-bottom: 15px;"><span style="display: inline-block;">💡</span> Tips Kelulusan</h4>', unsafe_allow_html=True)
    st.markdown("""
        <ol style="font-size: 0.9rem; padding-left: 20px;">
            <li><b>Jaga Konsistensi IPS</b> - Pertahankan IPS yang baik sejak semester awal</li>
            <li><b>Manajemen Waktu</b> - Bagi waktu antara kuliah, pekerjaan, dan kehidupan pribadi</li>
            <li><b>Aktif Konsultasi</b> - Konsultasi rutin dengan pembimbing akademik</li>
            <li><b>Perencanaan Studi</b> - Rencanakan pengambilan mata kuliah dengan bijak</li>
        </ol>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer dengan info developer
st.markdown("""
    <div class="footer">
        <p>
            <span style="font-weight: 600;">Prediksi Kelulusan Mahasiswa</span> dengan XGBoost<br>
            &copy; 2025 | <a href="#" style="color: #6C63FF; text-decoration: none;">Dokumentasi</a> | <a href="#" style="color: #6C63FF; text-decoration: none;">Kontak</a>
        </p>
        <p style="margin-top: 5px; font-size: 0.7rem;">
            Powered by AI & Machine Learning | v1.0.0
        </p>
    </div>
""", unsafe_allow_html=True)
