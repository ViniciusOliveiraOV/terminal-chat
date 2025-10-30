@echo off
echo ==================================================
echo 🚀 Terminal Chat - Setup para Deploy na Vercel
echo ==================================================
echo.

REM Verificar se é um repositório git
if not exist ".git" (
    echo 📁 Inicializando repositório Git...
    git init
    echo ✅ Git inicializado
) else (
    echo ✅ Repositório Git já existe
)

REM Adicionar arquivos
echo 📋 Adicionando arquivos ao Git...
git add .

REM Commit
echo 💾 Fazendo commit...
git commit -m "Terminal Chat - Ready for Vercel deployment - Complete chat application with authentication - Real-time messaging and voice chat - Email verification system - Cross-platform terminal client - Production-ready configuration - Vercel deployment files included"

echo ✅ Commit realizado

REM Instruções para o usuário
echo.
echo ==================================================
echo 🎯 Próximos passos:
echo ==================================================
echo 1. Crie um repositório no GitHub:
echo    https://github.com/new
echo.
echo 2. Execute os comandos abaixo com SEU usuário:
echo    git remote add origin https://github.com/SEU_USUARIO/terminal-chat.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Vá para Vercel e importe o projeto:
echo    https://vercel.com/new
echo.
echo 4. Configure as variáveis de ambiente na Vercel:
echo    SECRET_KEY=sua-chave-super-secreta
echo    EMAIL_USERNAME=viniciusrodrigueswork@gmail.com
echo    EMAIL_PASSWORD=txnywxuusljfeivk
echo    SERVER_BASE_URL=https://SEU-PROJETO.vercel.app
echo.
echo 5. Após deploy, atualize SERVER_BASE_URL com URL real
echo.
echo ==================================================
echo 📚 Documentação completa em:
echo    - VERCEL_DEPLOY.md
echo    - PRODUCTION.md
echo ==================================================
pause