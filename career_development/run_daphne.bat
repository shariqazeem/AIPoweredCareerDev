@echo off
setlocal
set DJANGO_SETTINGS_MODULE=career_development.settings
python -m daphne -b 0.0.0.0 -p 8000 career_development.asgi:application
endlocal
pause
