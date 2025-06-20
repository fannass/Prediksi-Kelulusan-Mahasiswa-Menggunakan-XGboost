import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# Set Page Configuration
st.set_page_config(
    page_title="Prediksi Kelulusan Mahasiswa",
    page_icon="🎓",
    layout="wide"
)

# Simple CSS untuk styling
st.markdown("""
<style>
    .main {
        background-color: #FAFAFA;
    }
    h1 {
        color: #1E88E5;
        font-weight: 600;
    }
    h3 {
        color: #333;
    }
    .highlight {
        background-color: #f0f7ff;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #1E88E5;
    }
    .footer {
        text-align: center;
        padding-top: 20px;
        color: #777;
        font-size: 14px;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        border-radius: 4px;
        padding: 10px 20px;
        font-weight: 600;
    }
    .result-box {
        padding: 20px;
        border-radius: 5px;
        margin-top: 20px;
        text-align: center;
    }
    .result-tepat {
        background-color: #e3fcef;
        border: 1px solid #00C897;
    }
    .result-terlambat {
        background-color: #ffe6e6;
        border: 1px solid #FF5555;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🎓 Prediksi Kelulusan Mahasiswa")
st.markdown("Sistem cerdas untuk memprediksi status kelulusan mahasiswa menggunakan algoritma XGBoost")

# Load the model
try:
    model_path = 'trained_model_xgboost.pkl'
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
except Exception as e:
    st.error(f"Error loading model: {str(e)}")
    model = None

# Sidebar input features
st.sidebar.header("📝 Input Data Mahasiswa")

def user_input_features():
    # Personal Information
    st.sidebar.subheader("Informasi Pribadi")
    jenis_kelamin = st.sidebar.selectbox("Jenis Kelamin", ("LAKI-LAKI", "PEREMPUAN"))
    status_mahasiswa = st.sidebar.selectbox("Status Mahasiswa", ("TIDAK BEKERJA", "BEKERJA"))
    status_nikah = st.sidebar.selectbox("Status Nikah", ("BELUM MENIKAH", "MENIKAH"))
    
    # Academic Information
    st.sidebar.subheader("Nilai Akademik")
    ips1 = st.sidebar.slider("IPS 1", 0.0, 4.0, 2.0, 0.01)
    ips2 = st.sidebar.slider("IPS 2", 0.0, 4.0, 2.0, 0.01)
    ips3 = st.sidebar.slider("IPS 3", 0.0, 4.0, 2.0, 0.01)
    ips4 = st.sidebar.slider("IPS 4", 0.0, 4.0, 2.0, 0.01)
    ips5 = st.sidebar.slider("IPS 5", 0.0, 4.0, 2.0, 0.01)

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
    st.subheader("📊 Data Mahasiswa")
    st.dataframe(input_df)
    
    # IPS Visualization
    st.subheader("📈 Tren Nilai IPS")
    
    # Create IPS trend chart
    ips_values = [input_df['IPS 1'].values[0], input_df['IPS 2'].values[0], 
                  input_df['IPS 3'].values[0], input_df['IPS 4'].values[0], 
                  input_df['IPS 5'].values[0]]
    semesters = ['Semester 1', 'Semester 2', 'Semester 3', 'Semester 4', 'Semester 5']
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(semesters, ips_values, marker='o', linewidth=2, color='#1E88E5')
    ax.set_ylim(0, 4.0)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_title('Tren Nilai IPS per Semester')
    
    # Calculate average IPS
    avg_ips = sum(ips_values) / len(ips_values)
    
    # Display average line
    ax.axhline(y=avg_ips, color='#FF5555', linestyle='--', alpha=0.8)
    ax.text(0, avg_ips + 0.05, f'Rata-rata: {avg_ips:.2f}', color='#FF5555')
    
    st.pyplot(fig)

with col2:
    # Encode input features for prediction
    input_df_encoded = input_df.copy()
    input_df_encoded['Jenis Kelamin'] = input_df_encoded['Jenis Kelamin'].map({'LAKI-LAKI': 0, 'PEREMPUAN': 1})
    input_df_encoded['Status Mahasiswa'] = input_df_encoded['Status Mahasiswa'].map({'TIDAK BEKERJA': 1, 'BEKERJA': 0})
    input_df_encoded['Status Nikah'] = input_df_encoded['Status Nikah'].map({'BELUM MENIKAH': 0, 'MENIKAH': 1})
    input_df_encoded.columns = ['JENIS KELAMIN', 'STATUS MAHASISWA', 'STATUS NIKAH', 'IPS 1', 'IPS 2', 'IPS 3', 'IPS 4', 'IPS 5']

    # Prediction button
    st.subheader("🔮 Hasil Prediksi")
    if st.button("Prediksi Status Kelulusan"):
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
                    st.balloons()  # Animation for positive result
                    st.markdown(f"""
                        <div class="result-box result-tepat">
                            <h3>TEPAT WAKTU ✅</h3>
                            <p>Kemungkinan kelulusan tepat waktu: {prob_tepat_waktu*100:.1f}%</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="result-box result-terlambat">
                            <h3>TERLAMBAT ⏰</h3>
                            <p>Kemungkinan kelulusan terlambat: {prob_terlambat*100:.1f}%</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.subheader("Faktor Utama Prediksi:")
                
                # Identify important factors
                faktor = []
                if input_df['IPS 1'].values[0] < 2.0:
                    faktor.append("⚠️ IPS 1 rendah")
                if input_df['IPS 5'].values[0] < 2.0:
                    faktor.append("⚠️ IPS 5 rendah")
                if input_df['Status Mahasiswa'].values[0] == "BEKERJA":
                    faktor.append("👨‍💼 Status bekerja")
                if input_df['Status Nikah'].values[0] == "MENIKAH":
                    faktor.append("💍 Status menikah")
                
                # If no specific factors detected
                if not faktor:
                    if avg_ips < 2.5:
                        faktor.append("⚠️ Rata-rata IPS rendah")
                    else:
                        faktor.append("📈 Performa akademik umum")
                
                # Display factors
                for f in faktor:
                    st.markdown(f"- {f}")
                
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
        <p>Prediksi Kelulusan Mahasiswa dengan XGBoost | © 2025</p>
    </div>
""", unsafe_allow_html=True)
