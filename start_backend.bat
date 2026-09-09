@echo off
setlocal
cd /d "%~dp0backend"

if not exist ".venv\Scripts\python.exe" (
  echo Creating backend virtual environment...
  python -m venv .venv
)

call ".venv\Scripts\activate.bat"
pip install -r requirements.txt
uvicorn app.main:app --reload
