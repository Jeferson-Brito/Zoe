@echo off
cd /d "%~dp0"
echo Iniciando Zoe...
echo.
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    echo Erro: Ambiente virtual nao encontrado!
    pause
    exit /b
)

python manage.py runserver
if %errorlevel% neq 0 (
    echo.
    echo O servidor parou com erro. Veja a mensagem acima.
)
echo.
pause
