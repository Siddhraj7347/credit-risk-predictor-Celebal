
<div align="center">

# 🔍 Credit Risk Predictor  
### Using Random Forest to Predict Creditworthiness  

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Built%20With-Streamlit-ff4b4b?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExb3hqMnZyNnU5dzdzZWltcmNraHRodGdsa3d6bWF5ZXN3YzAwN3o4aCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/l1J9EdzfOSgfyueLm/giphy.gif" width="500"/>

</div>

---

## 📌 Project Overview

This web app predicts **whether a person is creditworthy or not** based on financial and personal attributes using a **Random Forest classifier**.  
Built with 🧠 `scikit-learn`, 🖼 `Streamlit`, and styled using **custom dark mode themes**.

---

## 🧠 Model Info

- **Dataset**: [German Credit Data – UCI ML Repo](https://archive.ics.uci.edu/ml/datasets/statlog+(german+credit+data))
- **Model**: Random Forest Classifier (`scikit-learn`)
- **Features**: 20 attributes (age, employment, credit history, etc.)
- **Target**: Good or Bad Credit Risk

---

## 🚀 Features

- 🌐 Web app interface with **Streamlit**
- 🎨 Custom dark theme with gradient buttons
- 📊 Real-time predictions
- 💡 Intelligent preprocessing and feature encoding

---

## 📷 Demo Preview

> Replace this with your own gif or video  
<img src="demo.gif" alt="App demo" width="100%"/>

---

## 🛠 Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/yourusername/credit-risk-predictor.git
cd credit-risk-predictor
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

---

## ⚙️ Project Structure

```
📁 credit-risk-predictor
├── app.py                  # Main Streamlit app
├── model/
│   └── rf_model.pkl        # Trained Random Forest model
├── data/
│   └── german_credit.csv   # Raw dataset
├── requirements.txt
└── README.md
```

---

## 📈 Sample Prediction Logic

```python
import pandas as pd
import joblib

# Load trained model
model = joblib.load("model/rf_model.pkl")

# Example input
sample = pd.DataFrame([{
    'age': 35,
    'duration': 24,
    'credit_amount': 3000,
    'employment': '>=7 years',
    # ... add other features
}])

# Predict
prediction = model.predict(sample)
print("Creditworthy" if prediction[0] == 1 else "Not Creditworthy")
```

---

## 📦 requirements.txt

```text
streamlit
pandas
scikit-learn
joblib
```

---

## 🧾 License

Licensed under the [MIT License](LICENSE).

<div align="center">Made with ❤️ by [Siddhraj Gupta](https://github.com/Siddhraj7347</div>
