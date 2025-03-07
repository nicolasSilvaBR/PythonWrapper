@echo off

:: Save the current directory
set "ORIGINAL_DIR=%CD%"

:: Change to the directory where the script is located
cd /d "%~dp0"

:: Check if Python is installed
python --version >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not found in the PATH.
    echo Please install Python from https://www.python.org.
    pause
    exit /b 1
) else (
    echo Python is already installed.
)

:: Dynamically navigate to the libs folder based on the current script location
set "LIBS_DIR=%~dp0libs"

:: Ensure there are .whl files in the libs folder
echo Checking for .whl files in the libs folder...
if not exist "%LIBS_DIR%\*.whl" (
    echo No .whl files found in the libs folder. Please add the required wheel files.
    pause
    exit /b 1
)

:: Loop through each .whl file and install it
echo Installing dependencies from the libs folder...
for %%f in ("%LIBS_DIR%\*.whl") do (
    pip install --no-index --find-links="%LIBS_DIR%" "%%f"
    if %ERRORLEVEL% neq 0 (
        echo Failed to install dependency %%f.
        ::pause
        exit /b 1
    )
)

:: Ensure the directory contains main.py
if not exist "main.py" (
    echo main.py does not exist in the current directory.
    pause
    exit /b 1
)

:: Run the Streamlit application
echo Starting Streamlit application...
start "" cmd /k "streamlit run main.py"

:: Return to the original directory
cd /d "%ORIGINAL_DIR%"

pause
