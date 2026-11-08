@echo off
cd /d "%~dp0"
set PY=
where py >nul 2>nul && set PY=py
if not defined PY where python >nul 2>nul && set PY=python
if not defined PY goto :nopython
echo Using: %PY%
%PY% -m pip install pyinstaller
if errorlevel 1 goto :fail
%PY% -m PyInstaller --onefile --windowed --name MojibDehasher mojib_dehasher.py
if errorlevel 1 goto :fail
if not exist "dist\MojibDehasher.exe" goto :fail
echo.
echo done! your exe is: %cd%\dist\MojibDehasher.exe
pause
exit /b 0

:nopython
echo Python was not found. Install Python 3 from python.org and clik "Add python.exe to PATH" on the first screen,
echo then run this file again pls.
pause
exit /b 1

:fail
echo.
echo Build failed for some reason check above.
echo if it say python not found or open store install from python site.
pause
exit /b 1
