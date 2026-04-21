# 📚 Multilingual Automated Essay Grading System Using Machine Learning

## 📌 Overview

This project is an **Automated Essay Grading System** that evaluates essays using Machine Learning techniques.
It supports **multiple languages (English, Kannada, Tamil, Telugu)** and provides **real-time scores with feedback**.

---

## 🚀 Features

* Essay scoring (1–10 scale)
* Multilingual support
* Real-time processing
* Feedback (strengths & weaknesses)
* Grammar and sentiment analysis
* Readability metrics
* Plagiarism detection
* Report export (JSON/Text)

---

## 🛠️ Tech Stack

* **Backend:** Flask
* **Frontend:** Streamlit
* **ML Models:** Ridge Regression, BERT
* **Libraries:** scikit-learn, pandas, nltk, plotly

---

## 📂 Project Structure

```
AEGUML/
├── backend/
├── frontend/
├── training/
├── data/
├── models/
└── tests/
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/reddynayana708-code/AEGUML.git
cd AEGUML
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

### Activate:

* Windows:

```bash
.venv\Scripts\activate
```

* macOS/Linux:

```bash
source .venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Download NLTK Data

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

---

## ▶️ Run the Project

### Start Backend

```bash
python backend/app.py
```

### Start Frontend

```bash
streamlit run frontend/app.py
```

### Open in Browser

```
http://localhost:8501
```

---

## 📊 Usage

1. Select language
2. Enter essay
3. Click **Grade**
4. View score and feedback

---

## 🐛 Troubleshooting

### Port already in use

```bash
streamlit run frontend/app.py --server.port 8502
```

### Missing dependencies

```bash
pip install -r requirements.txt
```

---

## 📈 Performance

* Fast response time (<2 sec)
* Accurate scoring using ML models

---

## 🤝 Contributing

* Fork the repository
* Create a branch
* Make changes
* Submit pull request

---

## 📄 License

MIT License

---

## 👩‍💻 Author
Nayana 
