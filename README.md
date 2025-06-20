# Student Graduation Prediction with XGBoost

## 📚 Project Description
This project aims to develop a web-based machine learning application for predicting student graduation. Utilizing the *XGBoost* algorithm, this application is built with Python's *Streamlit* framework, providing an intuitive interface for users to input academic and demographic data and display prediction results in a user-friendly manner.

Presentation Link: [Machine Learning Implementation on Student Graduation Prediction](https://youtu.be/-vr4-vIRTJ0)

## 🎯 Project Goals
- **Identify Key Factors**: Analyze significant factors affecting on-time graduation.
- **Model Optimization**: Apply *hyperparameter tuning* to enhance model performance.
- **Interactive Web Application**: Create an easy-to-use web tool for predicting student graduation based on academic and demographic data.

## ⚙️ Key Features
- **Graduation Prediction**: High-accuracy model for predicting graduation status.
- **Feature Importance Visualization**: Display the contribution of each factor to the prediction.
- **User-Friendly Interface**: Interactive and accessible application built with Streamlit.

## 🛠 Project Structure
- `Prediksi Kelulusan XGBoost.ipynb`: Jupyter Notebook containing XGBoost model training and evaluation processes.
- `Prediksi Kelulusan.ipynb`: Original Jupyter Notebook containing Random Forest model training.
- `app.py`: Main file to run the **Streamlit** application.
- `trained_model_xgboost.pkl`: Pre-trained XGBoost model ready for predictions.
- `trained_model.pkl`: Original Random Forest model (not used in current version).
- `Kelulusan Train.xlsx`: Dataset used for model training.
- `requirements.txt`: List of dependencies needed to run this project.

## 🧪 Technologies Used
- **Python**: Primary programming language.
- **XGBoost**: For implementing the gradient boosting model.
- **Scikit-learn**: For data preparation and model evaluation.
- **Streamlit**: For building the user interface.
- **Pandas & NumPy**: For data processing and analysis.
- **Matplotlib & Seaborn**: For data visualization.

## 🔍 Dataset
The dataset used in this research is sourced from [Kaggle](https://www.kaggle.com/datasets/hafizhathallah/kelulusan-mahasiswa). Variables include gender, student status, marital status, and GPA (semesters 1-5), with graduation status as the target variable.

## 🚀 How to Run the Project
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Maurino23/prediksi-kelulusan-mahasiswa-streamlit.git
