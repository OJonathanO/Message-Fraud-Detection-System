@echo off
cd /d "%~dp0backend"
set PYTHONPATH=%~dp0
venv\Scripts\activate
python run.py
