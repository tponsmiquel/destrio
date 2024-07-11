@echo off
REM Cambiar al directorio donde se encuentra el script de Python
cd %~dp0

REM Ejecutar el script de Python
python app.py

REM Pausar para mantener la ventana abierta después de la ejecución
pause
