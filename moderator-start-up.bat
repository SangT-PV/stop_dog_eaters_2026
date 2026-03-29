@echo off
echo =======================================================
echo Starting Stop Dog Eaters Moderation Dashboard...
echo =======================================================
echo.

echo [1] Starting Website Server on http://localhost:8000...
start cmd /k "cd website && python -m http.server 8000"

echo [2] Starting Moderation API Server on http://localhost:5000...
start cmd /k "python automation/api_server.py"

echo [3] Opening Moderation Dashboard in your browser...
ping 127.0.0.1 -n 3 > nul
start http://localhost:8000/moderate.html

echo.
echo Setup Complete! 
echo Feel free to minimize these command windows. 
echo Close them when you are finished moderating!
pause
