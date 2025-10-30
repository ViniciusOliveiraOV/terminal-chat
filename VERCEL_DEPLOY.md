# Terminal Chat - Deploy na Vercel

## 🚀 Como fazer deploy na Vercel

### 1. Preparar o projeto no GitHub

```bash
# No seu terminal, na pasta do projeto:
git init
git add .
git commit -m "Initial commit - Terminal Chat"

# Criar repositório no GitHub e conectar:
git remote add origin https://github.com/SEU_USUARIO/terminal-chat.git
git branch -M main
git push -u origin main
```

### 2. Importar na Vercel

1. **Acesse**: https://vercel.com
2. **Faça login** com sua conta GitHub
3. **Clique em "New Project"**
4. **Selecione** o repositório `terminal-chat`
5. **Clique em "Import"**

### 3. Configurar Variáveis de Ambiente

Na Vercel, vá em **Settings → Environment Variables** e adicione:

```bash
# Obrigatórias
SECRET_KEY = sua-chave-super-secreta-aleatoria
EMAIL_USERNAME = dsgsdgdsgdsgdsgdsgds@gmail.com
EMAIL_PASSWORD = safsdfdsgfdsgsd
SERVER_BASE_URL = https://SEU-PROJETO.vercel.app

# Opcionais
EMAIL_FROM = Terminal Chat <viniciusrodrigueswork@gmail.com>
SMTP_SERVER = smtp.gmail.com
SMTP_PORT = 587
```

### 4. Deploy Automático

A Vercel irá automaticamente:
- ✅ Detectar que é um projeto Python
- ✅ Instalar dependências do `requirements.txt`
- ✅ Usar `server/main.py` como ponto de entrada
- ✅ Gerar um domínio como `seu-projeto.vercel.app`

### 5. Configuração Final

Após o deploy, **atualize a variável**:
```bash
SERVER_BASE_URL = https://terminal-chat-abc123.vercel.app
```

### 6. Testar o Deploy

1. **Acesse**: `https://seu-projeto.vercel.app/docs`
2. **Deveria mostrar**: A documentação da API do FastAPI
3. **Teste registro**: Crie uma conta para testar email

### 7. Configurar Domínio Personalizado (Opcional)

Na Vercel:
1. **Settings → Domains**
2. **Add Domain**: `chat.seudominio.com`
3. **Configure DNS** conforme instruções
4. **Atualize**: `SERVER_BASE_URL = https://chat.seudominio.com`

## 🎯 Arquivos Criados para Vercel

### `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "server/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "server/main.py"
    }
  ]
}
```

### `requirements.txt` (raiz do projeto)
- Lista todas as dependências necessárias
- Vercel instala automaticamente

## 🔧 Configurações Específicas da Vercel

### Banco de Dados
- **SQLite funciona** na Vercel (dados temporários)
- **Para dados permanentes**: considere PostgreSQL (PlanetScale, Supabase)

### WebSockets
- **Funciona** na Vercel com algumas limitações
- **Para uso intensivo**: considere Railway ou DigitalOcean

### Logs
- **Acesse logs** em: Vercel Dashboard → Project → Functions

## 🚨 Problemas Comuns

### ❌ Erro: "Module not found"
**Solução**: Verifique se todas as dependências estão em `requirements.txt`

### ❌ Erro: "Build failed"
**Solução**: Verifique se `server/main.py` existe e está correto

### ❌ Emails não funcionam
**Solução**: Verifique variáveis de ambiente na Vercel

### ❌ WebSocket não conecta
**Solução**: Use `wss://` em vez de `ws://` para HTTPS

## 📱 Atualizando o Cliente

Após o deploy, atualize o cliente:

```bash
# client/.env
SERVER_URL=https://seu-projeto.vercel.app
WEBSOCKET_URL=wss://seu-projeto.vercel.app
```

## ⚡ Deploy Alternativo (Railway)

Se a Vercel não funcionar bem para WebSockets:

```bash
# Instale Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

---

**🎉 Resultado**: Seu Terminal Chat estará online em `https://seu-projeto.vercel.app` com domínio personalizado e emails funcionando!