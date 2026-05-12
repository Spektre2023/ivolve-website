@echo off
REM Double-click this file to generate the next version of the Netlify manifest.
REM It auto-increments the version number based on existing
REM ivolve_netlify_manifest_v*.txt files in this folder.
REM
REM IMPORTANT: This .bat file and generate_netlify_manifest.py must be in the
REM SAME folder as the website assets you want to scan. The script scans its
REM own location, not wherever you happen to launch it from.

setlocal
cd /d "%~dp0"

set LOG=netlify_manifest_run_log.txt

echo. > "%LOG%"
echo =============================================================== >> "%LOG%"
echo   Ivolve Netlify Manifest Generator >> "%LOG%"
echo   %DATE% %TIME% >> "%LOG%"
echo   Scanning: %CD% >> "%LOG%"
echo =============================================================== >> "%LOG%"

echo.
echo ===============================================================
echo   Ivolve Netlify Manifest Generator
echo ===============================================================
echo.
echo Scanning: %CD%
echo.

REM Confirm the python script is sitting next to this .bat
if not exist "generate_netlify_manifest.py" (
    echo ERROR: generate_netlify_manifest.py is NOT in this folder.
    echo The .bat and the .py file must be together.
    echo Current folder: %CD%
    echo.
    echo ERROR: generate_netlify_manifest.py not found in %CD% >> "%LOG%"
    goto :done
)

REM Try `python` first, then `py` as fallback.
where python >nul 2>&1
if %errorlevel%==0 (
    python generate_netlify_manifest.py
    python generate_netlify_manifest.py >> "%LOG%" 2>&1
    goto :done
)

where py >nul 2>&1
if %errorlevel%==0 (
    py generate_netlify_manifest.py
    py generate_netlify_manifest.py >> "%LOG%" 2>&1
    goto :done
)

echo ERROR: Python is not installed (or not on PATH).
echo Install it from https://www.python.org/downloads/
echo IMPORTANT: tick "Add Python to PATH" during install.
echo ERROR: Python is not installed (or not on PATH). >> "%LOG%"

:done
echo.
echo ===============================================================
echo Done. Press any key to close this window.
echo (Full log saved to netlify_manifest_run_log.txt)
echo ===============================================================
pause >nul

endlocal
