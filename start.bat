@echo off
start "Backend" cmd /k "cd backend && python app.py"
timeout /t 5
start "Frontend" cmd /k "cd frontend && streamlit run app.py"