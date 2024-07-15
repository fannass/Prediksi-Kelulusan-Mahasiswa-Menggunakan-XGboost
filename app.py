import streamlit as st
import pandas as pd
import pickle

# Load trained model
model_path = 'trained_model.pkl'
with open(model_path, 'rb') as file:
    model = pickle.load(file)


# Title and Description
st.title("Prediksi Kelulusan Mahasiswa")
st.markdown("Aplikasi ini memprediksi apakah seorang mahasiswa akan lulus tepat waktu atau terlambat berdasarkan beberapa variabel independen.")

# Sidebar for user inputs
st.sidebar.header("Input Data Mahasiswa")

def user_input_features():
    jenis_kelamin = st.sidebar.selectbox("Jenis Kelamin", ("LAKI-LAKI", "PEREMPUAN"))
    status_mahasiswa = st.sidebar.selectbox("Status Mahasiswa", ("MAHASISWA", "BEKERJA"))
    status_nikah = st.sidebar.selectbox("Status Nikah", ("BELUM MENIKAH", "MENIKAH"))
    ips1 = st.sidebar.number_input("IPS 1", min_value=0.0, max_value=4.0, value=2.0, step=0.01)
    ips2 = st.sidebar.number_input("IPS 2", min_value=0.0, max_value=4.0, value=2.0, step=0.01)
    ips3 = st.sidebar.number_input("IPS 3", min_value=0.0, max_value=4.0, value=2.0, step=0.01)
    ips4 = st.sidebar.number_input("IPS 4", min_value=0.0, max_value=4.0, value=2.0, step=0.01)
    ips5 = st.sidebar.number_input("IPS 5", min_value=0.0, max_value=4.0, value=2.0, step=0.01)

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

input_df = user_input_features()

# Display user input before encoding
st.subheader("Input Data yang Anda Masukkan:")
st.write(input_df)

# Encode user input
input_df_encoded = input_df.copy()
input_df_encoded['Jenis Kelamin'] = input_df_encoded['Jenis Kelamin'].map({'LAKI-LAKI': 0, 'PEREMPUAN': 1})
input_df_encoded['Status Mahasiswa'] = input_df_encoded['Status Mahasiswa'].map({'MAHASISWA': 1, 'BEKERJA': 0})
input_df_encoded['Status Nikah'] = input_df_encoded['Status Nikah'].map({'BELUM MENIKAH': 0, 'MENIKAH': 1})
input_df_encoded.columns = ['JENIS KELAMIN', 'STATUS MAHASISWA', 'STATUS NIKAH', 'IPS 1', 'IPS 2', 'IPS 3', 'IPS 4', 'IPS 5']

# Prediction button
if st.button("Prediksi Kelulusan"):
    # Prediction
    prediction = model.predict(input_df_encoded)
    prediction_proba = model.predict_proba(input_df_encoded)
    
    # Display the prediction
    st.subheader("Prediksi Kelulusan:")
    kelulusan = "TEPAT WAKTU" if prediction[0] == 0 else "TERLAMBAT"

    if kelulusan == "TEPAT WAKTU":
        st.success(f"{kelulusan}")
    else:
        st.error(f"{kelulusan}")

    # Display the prediction probability
    st.subheader("Probabilitas Prediksi:")
    st.write(f"Probabilitas Tepat Waktu: {prediction_proba[0][0]*100:.2f}%")
    st.write(f"Probabilitas Terlambat: {prediction_proba[0][1]*100:.2f}%")

