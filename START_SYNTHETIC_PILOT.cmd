@echo off
cd /d "%~dp0"
py -3 -m scripts.investigation_app
if errorlevel 1 pause
