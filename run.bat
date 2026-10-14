@echo off
setlocal
title NoseClicker AI
cd /d "%~dp0"

set "PY_EXE="

python -c "import sys" >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set "PY_EXE=python"
    goto :found
)

py -c "import sys" >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set "PY_EXE=py"
    goto :found
)

python3 -c "import sys" >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set "PY_EXE=python3"
    goto :found
)

for /d %%D in ("%LOCALAPPDATA%\Python\python*") do (
    if exist "%%D\python.exe" (
        set "PY_EXE=%%D\python.exe"
        goto :found
    )
)

for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
    if exist "%%D\python.exe" (
        set "PY_EXE=%%D\python.exe"
        goto :found
    )
)

for /d %%D in ("%ProgramFiles%\Python*") do (
    if exist "%%D\python.exe" (
        set "PY_EXE=%%D\python.exe"
        goto :found
    )
)

for /d %%D in ("C:\Python*") do (
    if exist "%%D\python.exe" (
        set "PY_EXE=%%D\python.exe"
        goto :found
    )
)

:found
if defined PY_EXE (
    "%PY_EXE%" main.py %*
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo [!] Exited with error code %ERRORLEVEL%.
        pause
    )
    goto :end
)

echo.
echo [!] Python was not found automatically.
echo     Please open terminal in this folder and run:
echo     python main.py
echo.
pause

:end
