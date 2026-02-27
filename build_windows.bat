@echo off
setlocal

python -m pip install -r requirements.txt
python -m PyInstaller --name MinerU-GUI --windowed --onefile app.py

echo.
echo Build complete. EXE location:
echo dist\MinerU-GUI.exe
endlocal
