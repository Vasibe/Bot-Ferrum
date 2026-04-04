@echo off
echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo Instalando navegador Chromium para Playwright...
python -m playwright install chromium

echo.
echo Listo! Ya puedes correr el bot con: python main.py
pause
