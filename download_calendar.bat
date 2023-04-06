@echo off

REM Activar el entorno virtual de Python
call .venv\Scripts\activate.bat

REM Instalar dependencias (si es necesario)
pip install -r requirements.txt

REM Ejecutar el script de Python
python outlook_win32.py

REM Desactivar el entorno virtual de Python
call .venv\Scripts\deactivate.bat
