@echo off
REM Double-click launcher for the Multi-Agent Financial Advisor.
REM Place this file in the SAME folder as main.py, then just double-click it.

cd /d "%~dp0"

if not exist venv\Scripts\activate.bat (
    echo Could not find venv\Scripts\activate.bat
    echo Make sure this file is in the same folder as main.py, and that you
    echo already ran: python -m venv venv
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo ============================================
echo   Multi-Agent Financial Advisor
echo ============================================
echo.

set /p COMPANY=Enter company name (e.g. Tata Motors):
set /p BUDGET=Enter budget (numbers only, e.g. 100000):
set /p DURATION=Enter investment duration (e.g. 5 years):
set /p RISK=Enter risk profile (conservative/moderate/aggressive):

echo.
python main.py --company "%COMPANY%" --budget %BUDGET% --duration "%DURATION%" --risk %RISK% --save-json last_report.json

echo.
echo A copy of this report was also saved as last_report.json in this folder.
echo.
pause
