# 🚀 Project Setup Guide - Essay Grading System

## Prerequisites
- Python 3.10 or higher
- Windows operating system
- Internet connection (for model downloads)

## 📋 Step-by-Step Setup

### Step 1: Navigate to Project Directory
```bash
cd c:\Users\nayan\Downloads\aesprojectnew
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment
```bash
venv\Scripts\activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Train the ML Model
```bash
python training/train_model.py
```
*This will download BERT models (~80MB) and create trained model files in the `models/` directory.*

### Step 6: Start Backend Server
Open a **new terminal window** and run:
```bash
# Activate virtual environment first
venv\Scripts\activate

# Start backend server
python backend/app.py
```
*Backend will run on http://localhost:8000*

### Step 7: Start Frontend Application
Open a **third terminal window** and run:
```bash
# Activate virtual environment first
venv\Scripts\activate

# Start frontend
streamlit run frontend/app.py
```
*Frontend will run on http://localhost:8501*

### Step 8: Access the Application
Open your web browser and go to:
**http://localhost:8501**

## 🚀 Quick Start (Batch Files)

### Option 1: Use Provided Batch Files
```bash
# Start backend
start_backend.bat

# Start frontend  
start_frontend.bat
```

### Option 2: Use Main Run Script
```bash
python run.py
```

## 📁 Project Structure
```
aesprojectnew/
├── backend/
│   ├── app.py              # Flask API server
│   ├── validations.py      # Strict validation rules
│   ├── feedback_engine.py  # Feedback analysis
│   └── plagiarism.py       # Plagiarism detection
├── frontend/
│   └── app.py              # Streamlit web interface
├── training/
│   └── train_model.py      # ML model training
├── models/                 # Trained model files
├── tests/                  # Test files
├── requirements.txt        # Python dependencies
└── run.py                 # Main entry point
```

## 🔧 Troubleshooting

### Common Issues & Solutions

#### Issue 1: "ModuleNotFoundError"
**Solution**: Make sure virtual environment is activated
```bash
venv\Scripts\activate
```

#### Issue 2: Port Already in Use
**Solution**: Kill existing processes or change ports
```bash
# Find processes using ports 8000 or 8501
netstat -ano | findstr :8000
netstat -ano | findstr :8501

# Kill processes (replace PID with actual process ID)
taskkill /PID <PID> /F
```

#### Issue 3: Model Download Fails
**Solution**: Check internet connection and retry training
```bash
python training/train_model.py
```

#### Issue 4: Language Detection Errors
**Solution**: Install missing dependencies
```bash
pip install langdetect deep-translator
```

#### Issue 5: NLTK Data Missing
**Solution**: Download NLTK data manually
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon')"
```

#### Issue 6: NumPy/Pandas Compatibility Error
**Solution**: Fixed in updated requirements.txt
```bash
pip install -r requirements.txt --no-cache-dir
```
*The requirements.txt now includes compatible versions:*
- *NumPy: >=1.24.3,<2.0.0*
- *Pandas: >=1.5.3,<2.0.0*

## 🧪 Testing the System

### Test the API
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test grading endpoint
curl -X POST http://localhost:8000/grade ^
-H "Content-Type: application/json" ^
-d "{\"essay\":\"This is a test essay.\", \"selected_language\":\"en\"}"
```

### Run Unit Tests
```bash
pytest tests/ -v
```

### Test Validation System
```bash
python -c "
import sys
sys.path.append('backend')
from validations import EssayValidator
v = EssayValidator()
result = v.validate_language_requirement('Test essay', 'en')
print('Validation working:', result['is_valid'])
"
```

## 🌐 Access Points

Once running, you can access:

1. **Frontend Interface**: http://localhost:8501
2. **Backend API**: http://localhost:8000
3. **API Documentation**: http://localhost:8000/
4. **Health Check**: http://localhost:8000/health

## 📝 Usage Instructions

### Using the Web Interface
1. Open http://localhost:8501 in your browser
2. Select the essay language (STRICT: Essay must be in this language)
3. Paste your essay text
4. Click "Grade My Essay"
5. Review the comprehensive feedback

### API Usage
Send POST request to `/grade` endpoint:
```json
{
  "essay": "Your essay text here...",
  "selected_language": "en"
}
```

## 🔐 Important Notes

### Strict Validation Rules
- Essay language MUST match selected language
- Response generated ONLY in selected language
- No language mixing allowed
- Minimum 50 words required
- Minimum 3 sentences required

### Supported Languages
- **English (en)**: Default
- **Kannada (kn)**: ಕನ್ನಡ
- **Tamil (ta)**: தமிழ்
- **Telugu (te)**: తెలుగు

## 📊 System Requirements

### Minimum Requirements
- **Python**: 3.10+
- **RAM**: 4GB (8GB recommended)
- **Storage**: 2GB free space
- **Internet**: For model downloads

### Recommended Requirements
- **Python**: 3.11+
- **RAM**: 8GB+
- **Storage**: 5GB free space
- **GPU**: Optional, for faster model training

## 🎯 Next Steps

After successful setup:
1. Test with sample essays
2. Try different languages
3. Explore the validation features
4. Review the API documentation
5. Run the test suite

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Ensure ports 8000 and 8501 are available
4. Review the error messages carefully

---

**Happy Essay Grading! 🎓**
