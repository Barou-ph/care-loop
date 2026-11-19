@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start_care_loop.ps1"
if errorlevel 1 pause
