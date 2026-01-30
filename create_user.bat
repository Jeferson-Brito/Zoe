@echo off
call venv\Scripts\activate
python manage.py createsuperuser
pause
