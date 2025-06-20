# Dokumentasi Prediksi Kelulusan Mahasiswa dengan XGBoost

## Daftar Isi
1. [Pengenalan Project](#pengenalan-project)
2. [Struktur Project](#struktur-project)
3. [Penjelasan Metode XGBoost](#penjelasan-metode-xgboost)
4. [Alur Kerja Project](#alur-kerja-project)
5. [Persiapan Data](#persiapan-data)
6. [Pembuatan Model](#pembuatan-model)
7. [Evaluasi Model](#evaluasi-model)
8. [Implementasi Web App](#implementasi-web-app)
9. [Cara Menjalankan Project](#cara-menjalankan-project)
10. [Referensi](#referensi)

## Pengenalan Project

Project Prediksi Kelulusan Mahasiswa adalah aplikasi berbasis web yang menggunakan algoritma machine learning untuk memprediksi apakah seorang mahasiswa akan lulus tepat waktu atau terlambat. Project ini menggunakan model **XGBoost** untuk melakukan prediksi berdasarkan data akademik dan status pribadi mahasiswa.

Aplikasi ini dibuat menggunakan framework **Streamlit** yang memungkinkan pembuatan aplikasi web interaktif dengan Python secara mudah dan cepat. Tujuan utama dari project ini adalah untuk membantu institusi pendidikan dalam mengidentifikasi mahasiswa yang berisiko lulus terlambat, sehingga dapat dilakukan intervensi dini untuk membantu mereka.

## Struktur Project

```
prediksi-kelulusan-mahasiswa-streamlit/
├── app.py                       # File aplikasi Streamlit utama
├── Kelulusan Train.xlsx         # Dataset untuk training model
├── Prediksi Kelulusan.ipynb     # Notebook untuk model Random Forest (versi awal)
├── Prediksi Kelulusan XGBoost.ipynb  # Notebook untuk model XGBoost
├── README.md                    # Dokumentasi umum project
├── requirements.txt             # Daftar library yang diperlukan
└── trained_model_xgboost.pkl    # Model XGBoost terlatih
```

## Penjelasan Metode XGBoost

### Apa itu XGBoost?

**XGBoost** (Extreme Gradient Boosting) adalah algoritma machine learning berbasis *ensemble learning* yang merupakan implementasi yang dioptimalkan dari algoritma Gradient Boosting. XGBoost dikembangkan oleh Tianqi Chen dan merupakan salah satu algoritma machine learning yang paling populer karena performa dan efisiensinya yang tinggi.

### Cara Kerja XGBoost

XGBoost bekerja dengan prinsip **boosting**, yang merupakan teknik untuk meningkatkan performa model prediktif dengan menggabungkan beberapa model sederhana (biasanya decision tree) menjadi satu model yang kuat. Berikut adalah prinsip dasar kerja XGBoost:

1. **Sequential Learning**: XGBoost membangun model secara iteratif dan sekuensial. Setiap model baru fokus untuk memperbaiki kesalahan dari model sebelumnya.

2. **Weighted Decision Trees**: XGBoost menggunakan decision tree sebagai model dasar (*weak learners*). Setiap tree baru dilatih untuk memprediksi *residual* (kesalahan) dari tree sebelumnya.

3. **Gradient Descent Optimization**: XGBoost menggunakan algoritma gradient descent untuk meminimalkan loss function. Ini memungkinkan model untuk meningkatkan akurasi secara sistematis di setiap iterasi.

4. **Regularization**: Salah satu keunggulan XGBoost adalah adanya fitur regularisasi yang mencegah overfitting, sehingga model dapat digeneralisasi lebih baik untuk data baru.

### Keunggulan XGBoost

1. **Akurasi Tinggi**: XGBoost seringkali menghasilkan performa yang lebih baik dibandingkan algoritma tradisional seperti Random Forest.

2. **Penanganan Data yang Efisien**: XGBoost dapat menangani missing values secara otomatis dan bekerja dengan baik untuk berbagai jenis data.

3. **Regularisasi Bawaan**: Fitur regularisasi L1 (Lasso) dan L2 (Ridge) membantu mencegah overfitting.

4. **Paralelisasi**: XGBoost mendukung paralelisasi komputasi, yang mempercepat proses training pada hardware multi-core.

5. **Feature Importance**: XGBoost memberikan informasi tentang kepentingan relatif setiap fitur dalam membuat prediksi.

### Hyperparameter XGBoost

Dalam project ini, kami menggunakan *grid search* untuk menemukan kombinasi hyperparameter terbaik, dengan mempertimbangkan parameter-parameter berikut:

- `n_estimators`: Jumlah tree yang dibangun (50, 100, 200)
- `learning_rate`: Tingkat pembelajaran (0.01, 0.1, 0.2)
- `max_depth`: Kedalaman maksimum dari tree (3, 5, 7)
- `min_child_weight`: Berat minimum di node anak (1, 3, 5)
- `subsample`: Fraksi sampel yang digunakan untuk setiap tree (0.7, 0.8, 0.9)
- `colsample_bytree`: Fraksi fitur yang digunakan untuk setiap tree (0.7, 0.8, 0.9)
- `gamma`: Parameter regularisasi yang mengontrol pemangkasan tree (0, 0.1, 0.2)

## Alur Kerja Project

Project prediksi kelulusan mahasiswa dengan XGBoost ini memiliki alur kerja sebagai berikut:

1. **Pengumpulan Data**: Menggunakan dataset `Kelulusan Train.xlsx` yang berisi data akademik dan personal mahasiswa.

2. **Analisis dan Preprocessing Data**: Melakukan eksplorasi data, penanganan missing values, dan transformasi fitur kategorikal menjadi numerik.

3. **Pembuatan Model**: Melatih model XGBoost dengan hyperparameter tuning untuk mencapai performa terbaik.

4. **Evaluasi Model**: Mengevaluasi performa model dengan metrik akurasi dan confusion matrix.

5. **Penyimpanan Model**: Model terbaik disimpan sebagai `trained_model_xgboost.pkl` untuk digunakan dalam aplikasi.

6. **Implementasi Web App**: Membuat aplikasi web interaktif menggunakan Streamlit yang memanfaatkan model terlatih untuk prediksi real-time.

## Persiapan Data

### Dataset

Dataset yang digunakan berisi beberapa variabel penting:

- **Jenis Kelamin**: LAKI-LAKI atau PEREMPUAN
- **Status Mahasiswa**: BEKERJA atau TIDAK BEKERJA
- **Status Nikah**: MENIKAH atau BELUM MENIKAH
- **IPS 1-5**: Indeks Prestasi Semester 1 hingga 5
- **Status Kelulusan**: Tepat Waktu (0) atau Terlambat (1)

### Preprocessing

1. **Eliminasi Kolom**: Menghapus kolom yang tidak relevan (NAMA, UMUR) dan kolom yang tidak digunakan untuk prediksi (IPS 6, IPS 7, IPS 8, IPK).

2. **Penanganan Missing Values**: Memeriksa dan menangani data yang hilang jika ada.

3. **Penanganan Duplikat**: Memeriksa dan menghapus data duplikat.

4. **Label Encoding**: Mengubah variabel kategorikal menjadi numerik:
   - JENIS KELAMIN: LAKI-LAKI → 0, PEREMPUAN → 1
   - STATUS MAHASISWA: BEKERJA → 0, TIDAK BEKERJA → 1
   - STATUS NIKAH: BELUM MENIKAH → 0, MENIKAH → 1
   - STATUS KELULUSAN: TEPAT WAKTU → 0, TERLAMBAT → 1

## Pembuatan Model

### Pembagian Data

Data dibagi menjadi set pelatihan (80%) dan pengujian (20%) dengan `random_state=42` untuk memastikan hasil yang konsisten:

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

### Hyperparameter Tuning

Untuk mendapatkan model XGBoost terbaik, kami melakukan GridSearchCV dengan berbagai kombinasi hyperparameter:

```python
param_grid = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 5, 7],
    'min_child_weight': [1, 3, 5],
    'subsample': [0.7, 0.8, 0.9],
    'colsample_bytree': [0.7, 0.8, 0.9],
    'gamma': [0, 0.1, 0.2]
}

grid_search = GridSearchCV(estimator=xgb_model, param_grid=param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train, y_train)
best_params = grid_search.best_params_
```

### Training Model Final

Setelah menemukan hyperparameter terbaik, model final XGBoost dilatih:

```python
xgb_model = xgb.XGBClassifier(**best_params, random_state=42)
xgb_model.fit(X_train, y_train)
```

## Evaluasi Model

### Metrik Evaluasi

Model dievaluasi menggunakan beberapa metrik:

1. **Akurasi**: Persentase prediksi yang benar dari total prediksi.

2. **Confusion Matrix**: Matriks yang menunjukkan jumlah True Positives, False Positives, True Negatives, dan False Negatives.

3. **Feature Importance**: Analisis kontribusi setiap fitur terhadap hasil prediksi.

### Visualisasi Hasil

Hasil evaluasi model divisualisasikan menggunakan:

1. **Heatmap Confusion Matrix**: Menampilkan jumlah prediksi benar dan salah untuk setiap kelas.

2. **Bar Chart Feature Importance**: Menampilkan peringkat fitur berdasarkan kontribusinya terhadap model.

## Implementasi Web App

Aplikasi web dibuat menggunakan Streamlit untuk menyediakan antarmuka yang user-friendly:

### Komponen Aplikasi

1. **Form Input**: Bagian sidebar untuk memasukkan data mahasiswa.

2. **Visualisasi Input**: Tampilan data yang dimasukkan oleh pengguna.

3. **Hasil Prediksi**: Visualisasi hasil prediksi (TEPAT WAKTU/TERLAMBAT) beserta probabilitasnya.

### Alur Kerja Aplikasi

1. Pengguna memasukkan data mahasiswa melalui form.
2. Data diproses dan dikonversi ke format yang sesuai dengan input model.
3. Model XGBoost melakukan prediksi berdasarkan data input.
4. Hasil prediksi dan probabilitasnya ditampilkan dalam format yang mudah dipahami.

## Cara Menjalankan Project

### Prasyarat

1. Python 3.x
2. Library yang diperlukan (tercantum dalam `requirements.txt`):
   - numpy
   - pandas
   - streamlit
   - scikit-learn
   - xgboost
   - matplotlib
   - seaborn

### Langkah-langkah

1. **Clone repository** (jika menggunakan git):
   ```bash
   git clone https://github.com/username/prediksi-kelulusan-mahasiswa-streamlit.git
   cd prediksi-kelulusan-mahasiswa-streamlit
   ```

2. **Install dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Latih model XGBoost** (opsional, jika ingin melatih ulang model):
   - Jalankan notebook `Prediksi Kelulusan XGBoost.ipynb` secara berurutan

4. **Jalankan aplikasi Streamlit**:
   ```bash
   streamlit run app.py
   ```

5. **Akses aplikasi**:
   - Buka browser dan kunjungi `http://localhost:8501`

## Referensi

1. Chen, T., & Guestrin, C. (2016). [XGBoost: A Scalable Tree Boosting System](https://arxiv.org/abs/1603.02754). In Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '16).

2. [Dokumentasi Resmi XGBoost](https://xgboost.readthedocs.io/)

3. [Dokumentasi Streamlit](https://docs.streamlit.io/)

4. Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning: Data Mining, Inference, and Prediction. Springer Science & Business Media.

5. Dataset: [Kaggle - Kelulusan Mahasiswa](https://www.kaggle.com/datasets/hafizhathallah/kelulusan-mahasiswa)
