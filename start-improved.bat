@echo off
echo =================================
echo Terminal Chat - Quick Start
echo =================================
echo.

echo Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo Iniciando Terminal Chat Server...
cd server

REM Verificar se .env existe
if not exist .env (
    echo Criando configuracao do servidor...
    copy .env.example .env
    echo.
    echo IMPORTANTE: Edite o arquivo server\.env com suas configuracoes de email!
    echo Pressione qualquer tecla quando estiver pronto...
    pause
    echo.
)

echo Instalando dependencias do servidor...
pip install fastapi uvicorn websockets sqlalchemy bcrypt python-jose[cryptography] python-multipart pydantic[email] python-dotenv --quiet

echo Servidor iniciando em http://localhost:8000
start /B python main.py
timeout /t 3 /nobreak >nul

echo.
echo Iniciando Terminal Chat Client...
cd ..\client

REM Verificar se .env existe
if not exist .env (
    echo Criando configuracao do cliente...
    copy .env.example .env
)

echo Instalando dependencias do cliente...
pip install textual rich websockets requests pydantic python-dotenv --quiet

echo.
echo =================================
echo Terminal Chat esta pronto!
echo =================================
echo Servidor: http://localhost:8000
echo Cliente: Iniciando agora...
echo.

REM Iniciar cliente
python main.py

echo.
echo Obrigado por usar o Terminal Chat!
pause