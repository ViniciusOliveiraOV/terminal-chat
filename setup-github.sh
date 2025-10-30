#!/bin/bash

echo "=================================================="
echo "🚀 Terminal Chat - Setup para Deploy na Vercel"
echo "=================================================="
echo

# Verificar se é um repositório git
if [ ! -d ".git" ]; then
    echo "📁 Inicializando repositório Git..."
    git init
    echo "✅ Git inicializado"
else
    echo "✅ Repositório Git já existe"
fi

# Adicionar arquivos
echo "📋 Adicionando arquivos ao Git..."
git add .

# Commit
echo "💾 Fazendo commit..."
git commit -m "Terminal Chat - Ready for Vercel deployment"

echo "✅ Commit realizado"

# Instruções para o usuário
echo
echo "=================================================="
echo "🎯 Próximos passos:"
echo "=================================================="
echo "1. Crie um repositório no GitHub:"
echo "   https://github.com/new"
echo
echo "2. Conectando ao repositório GitHub..."
echo "   https://github.com/ViniciusOliveiraOV/terminal-chat"

# Configurar repositório remoto
echo "🔗 Configurando repositório remoto..."
git remote add origin https://github.com/ViniciusOliveiraOV/terminal-chat.git 2>/dev/null || echo "Remote já existe"
git branch -M main

echo "📤 Fazendo push para GitHub..."
git push -u origin main
echo
echo "3. Vá para Vercel e importe o projeto:"
echo "   https://vercel.com/new"
echo
echo "4. Configure as variáveis de ambiente na Vercel:"
echo "   SECRET_KEY=sua-chave-super-secreta"
echo "   EMAIL_USERNAME=viniciusrodrigueswork@gmail.com"
echo "   EMAIL_PASSWORD=txnywxuusljfeivk"
echo "   SERVER_BASE_URL=https://SEU-PROJETO.vercel.app"
echo
echo "5. Após deploy, atualize SERVER_BASE_URL com URL real"
echo
echo "=================================================="
echo "📚 Documentação completa em:"
echo "   - VERCEL_DEPLOY.md"
echo "   - PRODUCTION.md"
echo "=================================================="