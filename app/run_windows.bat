@echo off
cd /d "%~dp0"
where py >nul 2>nul && (py q2_plotter.py) || (python q2_plotter.py)
pause
