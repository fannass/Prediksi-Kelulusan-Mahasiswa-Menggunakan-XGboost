# Dokumentasi Prediksi Kelulusan Mahasiswa dengan XGBoost

## Daftar Isi
1. [Pengenalan Project](#pengenalan-project)
2. [Struktur Project](#struktur-project)
3. [Penjelasan Metode XGBoost](#penjelasan-metode-xgboost)
4. [Alur Kerja Project](#alur-kerja-project)
5. [Persiapan Data](#persiapan-data)
6. [Pembuatan Model](#pembuatan-model)
7. [Evaluasi Model](#evaluasi-model)
8. [Implementasi Web App (main.py)](#implementasi-web-app-mainpy)
9. [Penjelasan UI/UX dan Dark Mode](#penjelasan-uiux-dan-dark-mode)
10. [Cara Menjalankan Project](#cara-menjalankan-project)
11. [Referensi](#referensi)

## Pengenalan Project

Project Prediksi Kelulusan Mahasiswa adalah aplikasi berbasis web yang menggunakan algoritma machine learning (XGBoost) untuk memprediksi apakah seorang mahasiswa akan lulus tepat waktu atau terlambat. Aplikasi ini dibuat dengan framework **Streamlit** dan menampilkan antarmuka modern, interaktif, serta responsif dengan dark mode.

## Struktur Project

```
prediksi-kelulusan-mahasiswa-streamlit/
├── DOKUMENTASI.md                # Dokumentasi lengkap project (file ini)
├── Kelulusan Train.xlsx          # Dataset untuk training model
├── main.py                       # File aplikasi Streamlit utama (DARK MODE, UI/UX modern)
├── Prediksi Kelulusan XGBoost.ipynb  # Notebook training & evaluasi model XGBoost
├── README.md                     # Dokumentasi umum project
├── requirements.txt              # Daftar library yang diperlukan
├── trained_model_xgboost.pkl     # Model XGBoost terlatih
├── trained_model.pkl             # Model lain (opsional, tidak digunakan di main.py)
```

> **Catatan:** File `app.py`, `app_fixed.py`, dan `app_optimized.py` sudah dihapus. Semua aplikasi web kini terpusat di `main.py`.

## Penjelasan Metode XGBoost

**XGBoost** (Extreme Gradient Boosting) adalah algoritma machine learning berbasis ensemble yang sangat populer untuk klasifikasi dan regresi. XGBoost membangun banyak decision tree secara bertahap, di mana setiap tree baru memperbaiki kesalahan dari tree sebelumnya. Model ini sangat efisien, mendukung regularisasi (mencegah overfitting), dan dapat menangani data dengan missing value.

### Cara Kerja XGBoost
1. **Boosting**: Model dibangun secara berurutan, setiap model baru memperbaiki error model sebelumnya.
2. **Decision Tree**: Model dasar adalah decision tree.
3. **Gradient Descent**: Optimasi dilakukan dengan menurunkan loss function.
4. **Regularisasi**: Ada penalti untuk model yang terlalu kompleks.

### Keunggulan XGBoost
- Akurasi tinggi
- Efisien dan cepat
- Mendukung regularisasi
- Dapat menangani missing value
- Mendukung feature importance

## Alur Kerja Project

1. **Pengumpulan Data**: Dataset `Kelulusan Train.xlsx` berisi data mahasiswa (jenis kelamin, status kerja, status nikah, IPS 1-5, status kelulusan).
2. **Preprocessing**: Data dibersihkan, fitur kategorikal di-encode ke numerik.
3. **Training Model**: Model XGBoost dilatih di notebook `Prediksi Kelulusan XGBoost.ipynb` dengan hyperparameter tuning (GridSearchCV).
4. **Evaluasi Model**: Model dievaluasi dengan akurasi, confusion matrix, dan feature importance.
5. **Simpan Model**: Model terbaik disimpan sebagai `trained_model_xgboost.pkl`.
6. **Implementasi Web App**: File `main.py` memuat model dan menyediakan antarmuka prediksi interaktif.

## Persiapan Data

- **Fitur**: Jenis Kelamin, Status Mahasiswa, Status Nikah, IPS 1-5
- **Target**: Status Kelulusan (0 = Tepat Waktu, 1 = Terlambat)
- **Preprocessing**: Label encoding untuk fitur kategorikal, normalisasi nilai IPS jika diperlukan.

## Pembuatan Model

- **Split Data**: 80% training, 20% testing
- **GridSearchCV**: Untuk mencari kombinasi hyperparameter terbaik
- **Training**: Model XGBoost dilatih dengan parameter terbaik
- **Simpan Model**: Model disimpan ke file `trained_model_xgboost.pkl`

## Evaluasi Model

- **Akurasi**: Persentase prediksi benar
- **Confusion Matrix**: Matriks prediksi benar/salah
- **Feature Importance**: Fitur mana yang paling berpengaruh
- **Visualisasi**: Heatmap confusion matrix, bar chart feature importance (di notebook)

## Implementasi Web App (main.py)

### Deskripsi File `main.py`
- **Fungsi utama**: Menyediakan aplikasi web interaktif untuk prediksi kelulusan mahasiswa berbasis model XGBoost.
- **Framework**: Streamlit
- **Fitur utama**:
  - Input data mahasiswa (jenis kelamin, status kerja, status nikah, IPS 1-5) melalui sidebar
  - Visualisasi data input dan tren IPS
  - Prediksi status kelulusan (tepat waktu/terlambat) beserta probabilitasnya
  - Penjelasan faktor utama yang mempengaruhi prediksi
  - UI/UX modern dengan dark mode

### Alur Kerja Aplikasi
1. **User mengisi data mahasiswa** di sidebar (dengan tooltip dan grouping card)
2. **Data divisualisasikan** di main area (tabel dan grafik tren IPS)
3. **User klik tombol prediksi**
4. **Model XGBoost melakukan prediksi** berdasarkan input user
5. **Hasil prediksi** (tepat waktu/terlambat) dan probabilitas ditampilkan dengan animasi, badge, dan faktor utama
6. **Faktor utama** (misal: IPS rendah, status bekerja/menikah) ditampilkan dalam bentuk badge warna-warni
7. **Footer** berisi link ke dokumentasi/repo

### Penjelasan Prediksi di main.py
- Input user di-encode ke format numerik sesuai model
- Model XGBoost (`trained_model_xgboost.pkl`) melakukan prediksi dan probabilitas
- Hasil prediksi:
  - **Tepat Waktu**: Jika output model 0
  - **Terlambat**: Jika output model 1
- Probabilitas ditampilkan dalam persen
- Faktor utama diidentifikasi dari input (misal: IPS rendah, status bekerja/menikah)
- Semua hasil ditampilkan dengan styling modern dan animasi

## Penjelasan UI/UX dan Dark Mode

- **Dark Mode**: Seluruh aplikasi (sidebar, main area, tabel, chart, tombol) menggunakan warna gelap yang konsisten dan nyaman di mata
- **Sidebar**: Input dibungkus dalam card, ada logo/ikon di atas, tooltip pada setiap input
- **Section**: Judul section diberi ikon (emoji)
- **Tombol**: Lebih besar, warna kontras, ada ikon, efek hover
- **Result Box**: Animasi fade-in, badge "Sukses"/"Perlu Perhatian", ikon besar
- **Faktor Utama**: Ditampilkan dalam bentuk badge warna-warni
- **Tabel**: Lebar penuh, efek shadow dan border-radius
- **Footer**: Ada link ke dokumentasi/repo
- **Animasi**: Hasil prediksi muncul dengan animasi fade-in

## Cara Menjalankan Project

### Prasyarat
- Python 3.x
- Library: numpy, pandas, streamlit, scikit-learn, xgboost, matplotlib, seaborn (lihat `requirements.txt`)

### Langkah-langkah
1. **Clone repository**
   ```bash
   git clone https://github.com/fannass/Prediksi-Kelulusan-Mahasiswa-Menggunakan-XGboost.git
   cd prediksi-kelulusan-mahasiswa-streamlit
   ```
2. **Install dependensi**
   ```bash
   pip install -r requirements.txt
   ```
3. **Latih model XGBoost** (opsional, jika ingin melatih ulang model):
   - Jalankan notebook `Prediksi Kelulusan XGBoost.ipynb`
4. **Jalankan aplikasi Streamlit**
   ```bash
   streamlit run main.py
   ```
5. **Akses aplikasi**
   - Buka browser ke `http://localhost:8501`

## Referensi

1. Chen, T., & Guestrin, C. (2016). [XGBoost: A Scalable Tree Boosting System](https://arxiv.org/abs/1603.02754).
2. [Dokumentasi Resmi XGBoost](https://xgboost.readthedocs.io/)
3. [Dokumentasi Streamlit](https://docs.streamlit.io/)
4. Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning.
5. Dataset: [Kaggle - Kelulusan Mahasiswa](https://www.kaggle.com/datasets/hafizhathallah/kelulusan-mahasiswa)
