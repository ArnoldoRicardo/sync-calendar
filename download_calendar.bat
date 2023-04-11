@echo off

set CURRENT_DIR=C:\Users\arnoldo.hernandez\dev\sync-calendar
set VENV_PATH=%CURRENT_DIR%\.venv
set SCRIPT_PATH=%CURRENT_DIR%\outlook_win32.py


REM Activar el entorno virtual de Python
call %VENV_PATH%\Scripts\activate.bat

REM Instalar dependencias (si es necesario)
pip install -r %CURRENT_DIR%\requirements.txt

REM Ejecutar el script de Python
python %SCRIPT_PATH%


REM Desactivar el entorno virtual de Python
call %VENV_PATH%\Scripts\deactivate.bat