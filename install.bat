@echo off
:: 1. Create fresh virtual environment
python -m venv venv
call venv\Scripts\activate.bat

:: 2. Install core dependencies
pip install --upgrade pip
pip install nextcord python-dotenv ffmpeg-python

:: 3. Install pre-built Whisper (no compilation)
pip install whisper-ctranslate2

echo Installation complete! Run with: python main.py
pause