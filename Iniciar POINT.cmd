@echo off
set PYTHONUTF8=1
if not exist "%~dp0.venv\Scripts\python.exe" (
  echo Primero prepara el entorno siguiendo DEPLOYMENT.md.
  pause
  exit /b 1
)
"%~dp0.venv\Scripts\python.exe" "%~dp0infrastructure\scripts\local.py" setup
if errorlevel 1 (
  pause
  exit /b 1
)
"%~dp0.venv\Scripts\python.exe" "%~dp0infrastructure\scripts\local.py" migrate
if errorlevel 1 (
  pause
  exit /b 1
)
"%~dp0.venv\Scripts\python.exe" "%~dp0infrastructure\scripts\dev.py"
pause
