import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# Set Page Configuration
st.set_page_config(
    page_title="Prediksi Kelulusan Mahasiswa",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS untuk styling (DARK THEME)
st.markdown("""
<style>
    :root {
        --primary: #1976D2;
        --primary-light: #42A5F5;
        --primary-dark: #0D47A1;
        --accent: #FF9800;
        --success: #43A047;
        --danger: #E53935;
        --warning: #FFA000;
        --background: #181A1B;
        --background-light: #23272B;
        --text: #F5F5F5;
        --text-light: #B0B3B8;
        --gray-light: #23272B;
        --gray-medium: #31363B;
    }
    
    body, .main, .block-container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: var(--text);
        background-color: var(--background) !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"], section[data-testid="stSidebar"] {
        background-color: var(--background-light) !important;
        color: var(--text);
        border-right: 1px solid var(--gray-medium);
    }
    .sidebar .sidebar-content {
        background-color: var(--background-light);
        color: var(--text);
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: var(--primary);
        font-weight: 700;
    }
    h1 {
        font-size: 2.2rem;
        margin-bottom: 0.8rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--primary-light);
        letter-spacing: -0.5px;
    }
    
    /* Text Elements */
    p, li, label, div, span {
        color: var(--text);
        line-height: 1.6;
    }
    
    /* Card Styling */
    .card, .chart-container, .factor-box, .highlight {
        background-color: var(--background-light);
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        padding: 20px;
        margin-bottom: 24px;
        border: 1px solid var(--gray-medium);
        color: var(--text);
    }
    .card:hover {
        box-shadow: 0 6px 16px rgba(0,0,0,0.35);
        transform: translateY(-2px);
    }
    
    /* Highlight Box */
    .highlight {
        background-color: #22304A;
        border-left: 6px solid var(--primary-light);
        color: var(--text);
        box-shadow: 0 2px 10px rgba(25, 118, 210, 0.15);
    }
    .highlight p {
        color: var(--text);
    }
    .highlight strong, .highlight b {
        color: var(--primary);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding-top: 30px;
        padding-bottom: 20px;
        color: var(--text-light);
        font-size: 0.9rem;
        border-top: 1px solid var(--gray-medium);
        margin-top: 40px;
        background: none;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: var(--primary);
        color: #fff;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
        width: 100%;
        font-size: 1.05rem;
        height: auto;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 2px 8px rgba(25, 118, 210, 0.15);
    }
    .stButton>button:hover {
        background-color: var(--primary-dark);
        box-shadow: 0 4px 12px rgba(25, 118, 210, 0.25);
        transform: translateY(-2px);
    }
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Result Boxes */
    .result-box {
        padding: 24px;
        border-radius: 12px;
        margin-top: 24px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        transition: all 0.3s ease;
        background-color: var(--background-light);
        color: var(--text);
    }
    .result-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.35);
    }
    .result-box h3 {
        margin: 0 0 16px 0;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .result-box p {
        font-size: 1.1rem;
        color: var(--text);
        margin-bottom: 0;
    }
    .result-tepat {
        background-color: #1B3C2B;
        border: 2px solid var(--success);
    }
    .result-tepat h3 {
        color: var(--success);
    }
    .result-terlambat {
        background-color: #3A2323;
        border: 2px solid var(--danger);
    }
    .result-terlambat h3 {
        color: var(--danger);
    }
    
    /* Data Table Styling */
    .dataframe-container {
        margin: 20px 0;
        border-radius: 10px;
        overflow: hidden !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.18);
        background-color: var(--background-light);
    }
    .dataframe {
        width: 100%;
        border-collapse: collapse !important;
        font-size: 15px !important;
        overflow: hidden !important;
        background-color: var(--background-light) !important;
        color: var(--text) !important;
    }
    .dataframe th {
        background-color: var(--primary-dark) !important;
        color: #fff !important;
        font-weight: 600 !important;
        padding: 12px 16px !important;
        text-align: center !important;
        border: none !important;
    }
    .dataframe td {
        color: var(--text) !important;
        padding: 10px 16px !important;
        border-bottom: 1px solid var(--gray-medium) !important;
        background-color: var(--background-light) !important;
    }
    .dataframe tr:nth-child(even) td {
        background-color: #23272B !important;
    }
    .dataframe tr:hover td {
        background-color: #22304A !important;
    }
    
    /* Slider Customization */
    .stSlider > div > div > div {
        background-color: var(--primary-light) !important;
    }
    
    /* Progress Bar Styling */
    .stProgress > div > div > div {
        background-color: var(--primary) !important;
    }
    
    /* Info Box */
    .stAlert {
        background-color: #22304A !important;
        color: var(--text) !important;
    }
    .st-ae {
        border-left-color: var(--primary-light) !important;
    }
    
    /* Factor Box */
    .factor-box {
        background-color: #23272B;
        border-left: 5px solid var(--primary-light);
        color: var(--text);
    }
    .factor-box h4 {
        color: var(--primary);
    }
    .factor-box ul {
        color: var(--text);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style='display: flex; align-items: center;'>
    <span style='font-size:2.5rem;margin-right:10px;'>🎓</span>
    <h1 style='margin-bottom:0;'>Prediksi Kelulusan Mahasiswa</h1>
</div>
<hr style='border: 1px solid #31363B; margin-top: 0.5rem; margin-bottom: 1.5rem;'>
""", unsafe_allow_html=True)
st.markdown("<span style='color:#B0B3B8;'>Sistem cerdas untuk memprediksi status kelulusan mahasiswa menggunakan algoritma XGBoost</span>", unsafe_allow_html=True)

# Load the model
try:
    model_path = 'trained_model_xgboost.pkl'
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
except Exception as e:
    st.error(f"Error loading model: {str(e)}")
    model = None

# Sidebar input features
st.sidebar.markdown("""
<div style='text-align:center; margin-bottom:1.5rem;'>
    <img src='https://img.icons8.com/ios-filled/100/1976D2/graduation-cap.png' width='60' style='margin-bottom:0.5rem;'>
    <h2 style='color:#42A5F5;'>Input Data Mahasiswa</h2>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<div class='card' style='padding:18px 12px 12px 12px;'>", unsafe_allow_html=True)
st.sidebar.subheader("🧑‍🎓 Informasi Pribadi")
jenis_kelamin = st.sidebar.selectbox("Jenis Kelamin", ("LAKI-LAKI", "PEREMPUAN"), help="Pilih jenis kelamin mahasiswa.")
status_mahasiswa = st.sidebar.selectbox("Status Mahasiswa", ("TIDAK BEKERJA", "BEKERJA"), help="Apakah mahasiswa bekerja saat kuliah?")
status_nikah = st.sidebar.selectbox("Status Nikah", ("BELUM MENIKAH", "MENIKAH"), help="Status pernikahan mahasiswa.")
st.sidebar.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown("<div class='card' style='padding:18px 12px 12px 12px;'>", unsafe_allow_html=True)
st.sidebar.subheader("📚 Nilai Akademik")
ips1 = st.sidebar.slider("IPS 1", 0.0, 4.0, 2.0, 0.01, help="Indeks Prestasi Semester 1")
ips2 = st.sidebar.slider("IPS 2", 0.0, 4.0, 2.0, 0.01, help="Indeks Prestasi Semester 2")
ips3 = st.sidebar.slider("IPS 3", 0.0, 4.0, 2.0, 0.01, help="Indeks Prestasi Semester 3")
ips4 = st.sidebar.slider("IPS 4", 0.0, 4.0, 2.0, 0.01, help="Indeks Prestasi Semester 4")
ips5 = st.sidebar.slider("IPS 5", 0.0, 4.0, 2.0, 0.01, help="Indeks Prestasi Semester 5")
st.sidebar.markdown("</div>", unsafe_allow_html=True)

def user_input_features():
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

# Get user input
input_df = user_input_features()

# Main panel
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <h2 style='display:flex;align-items:center;gap:8px;'>📊 Data Mahasiswa</h2>
    """, unsafe_allow_html=True)
    st.dataframe(input_df, use_container_width=True)
    
    # IPS Visualization
    st.markdown("""
    <h2 style='display:flex;align-items:center;gap:8px;'>📈 Tren Nilai IPS</h2>
    """, unsafe_allow_html=True)
    
    # Create IPS trend chart
    ips_values = [input_df['IPS 1'].values[0], input_df['IPS 2'].values[0], 
                  input_df['IPS 3'].values[0], input_df['IPS 4'].values[0], 
                  input_df['IPS 5'].values[0]]
    semesters = ['Semester 1', 'Semester 2', 'Semester 3', 'Semester 4', 'Semester 5']
    
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Set background color for better readability
    fig.patch.set_facecolor('#181A1B')
    ax.set_facecolor('#23272B')
    
    # Plot IPS trend line with improved visibility
    ax.plot(semesters, ips_values, marker='o', linewidth=2.5, color='#42A5F5', markerfacecolor='#42A5F5', markersize=8)
    ax.set_ylim(0, 4.0)
    ax.grid(True, linestyle='--', alpha=0.7, color='#31363B')
    
    # Improve axis labels and title
    ax.set_title('Tren Nilai IPS per Semester', fontsize=14, fontweight='bold', color='#42A5F5')
    ax.tick_params(axis='both', colors='#F5F5F5', labelsize=10)
    
    # Calculate average IPS
    avg_ips = sum(ips_values) / len(ips_values)
    
    # Display average line with improved visibility
    ax.axhline(y=avg_ips, color='#E53935', linestyle='--', linewidth=2, alpha=0.8)
    ax.text(0, avg_ips + 0.1, f'Rata-rata: {avg_ips:.2f}', color='#E53935', fontsize=12, fontweight='bold')
    
    st.pyplot(fig)

with col2:
    st.markdown("""
    <h2 style='display:flex;align-items:center;gap:8px;'>✨ Hasil Prediksi</h2>
    """, unsafe_allow_html=True)
    # Encode input features for prediction
    input_df_encoded = input_df.copy()
    input_df_encoded['Jenis Kelamin'] = input_df_encoded['Jenis Kelamin'].map({'LAKI-LAKI': 0, 'PEREMPUAN': 1})
    input_df_encoded['Status Mahasiswa'] = input_df_encoded['Status Mahasiswa'].map({'TIDAK BEKERJA': 1, 'BEKERJA': 0})
    input_df_encoded['Status Nikah'] = input_df_encoded['Status Nikah'].map({'BELUM MENIKAH': 0, 'MENIKAH': 1})
    input_df_encoded.columns = ['JENIS KELAMIN', 'STATUS MAHASISWA', 'STATUS NIKAH', 'IPS 1', 'IPS 2', 'IPS 3', 'IPS 4', 'IPS 5']

    # Prediction button
    if st.button("🔮 Prediksi Status Kelulusan", use_container_width=True):
        if model is not None:
            try:
                prediction = model.predict(input_df_encoded)
                prediction_proba = model.predict_proba(input_df_encoded)

                kelulusan = "TEPAT WAKTU" if prediction[0] == 0 else "TERLAMBAT"
                
                # Convert float32 to Python float
                prob_tepat_waktu = float(prediction_proba[0][0])
                prob_terlambat = float(prediction_proba[0][1])

                # Display prediction result
                if kelulusan == "TEPAT WAKTU":
                    st.balloons()
                    st.markdown(f"""
                    <div class="result-box result-tepat" style="animation: fadeIn 0.7s;">
                        <span style='font-size:2.2rem;'>✅</span>
                        <h3>TEPAT WAKTU</h3>
                        <span style='background:#43A047;color:#fff;padding:2px 12px;border-radius:12px;font-size:1rem;'>Sukses</span>
                        <p style='margin-top:10px;'>Kemungkinan kelulusan tepat waktu: <b>{prob_tepat_waktu*100:.1f}%</b></p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-box result-terlambat" style="animation: fadeIn 0.7s;">
                        <span style='font-size:2.2rem;'>⏰</span>
                        <h3>TERLAMBAT</h3>
                        <span style='background:#E53935;color:#fff;padding:2px 12px;border-radius:12px;font-size:1rem;'>Perlu Perhatian</span>
                        <p style='margin-top:10px;'>Kemungkinan kelulusan terlambat: <b>{prob_terlambat*100:.1f}%</b></p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.subheader("Faktor Utama Prediksi:")
                # Identify important factors
                faktor = []
                if input_df['IPS 1'].values[0] < 2.0:
                    faktor.append(("⚠️ IPS 1 rendah", "#E53935"))
                if input_df['IPS 5'].values[0] < 2.0:
                    faktor.append(("⚠️ IPS 5 rendah", "#E53935"))
                if input_df['Status Mahasiswa'].values[0] == "BEKERJA":
                    faktor.append(("👨‍💼 Status bekerja", "#FFA000"))
                if input_df['Status Nikah'].values[0] == "MENIKAH":
                    faktor.append(("💍 Status menikah", "#42A5F5"))
                if not faktor:
                    if avg_ips < 2.5:
                        faktor.append(("⚠️ Rata-rata IPS rendah", "#E53935"))
                    else:
                        faktor.append(("📈 Performa akademik umum", "#43A047"))
                st.markdown("<div style='margin-top:10px;'>", unsafe_allow_html=True)
                for f, color in faktor:
                    st.markdown(f"<span style='display:inline-block;background:{color};color:#fff;padding:6px 16px;border-radius:16px;margin:4px 4px 4px 0;font-size:1rem;'>{f}</span>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                st.info("💡 Prediksi ini berdasarkan model XGBoost yang dilatih dengan data historis mahasiswa.")
            
            except Exception as e:
                st.error(f"Error during prediction: {str(e)}")
        else:
            st.error("Model tidak tersedia. Silakan periksa file model.")

# Add information about XGBoost
st.markdown("### ℹ️ Tentang Model")
st.markdown("""
<div class="highlight">
    <p>Sistem ini menggunakan algoritma <b>XGBoost</b> (Extreme Gradient Boosting), 
    sebuah metode machine learning berbasis ensemble yang sangat efektif untuk 
    prediksi klasifikasi. Model ini dilatih dengan data historis mahasiswa dan mampu
    mengidentifikasi pola-pola yang berkaitan dengan kelulusan tepat waktu.</p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>Prediksi Kelulusan Mahasiswa dengan XGBoost | © 2025 &nbsp;|&nbsp; <a href='https://github.com/' style='color:#42A5F5;text-decoration:underline;' target='_blank'>Dokumentasi & Repo</a></p>
</div>
<style>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)
