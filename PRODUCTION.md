# Terminal Chat - Guia de Produção

## 🚀 Configuração para Produção

### 1. Configurações Essenciais (.env)

```bash
# ⚠️ ALTERE ESTAS CONFIGURAÇÕES PARA PRODUÇÃO!

# Segurança
SECRET_KEY=sua-chave-super-secreta-aleatoria-de-32-caracteres-ou-mais
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Base de Dados
DATABASE_URL=sqlite:///./chat.db
# Para PostgreSQL: postgresql://usuario:senha@localhost/terminal_chat
# Para MySQL: mysql://usuario:senha@localhost/terminal_chat

# Email (Gmail de Produção)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=suaempresa@gmail.com
EMAIL_PASSWORD=sua-senha-de-app-do-gmail
FROM_EMAIL=Terminal Chat <suaempresa@gmail.com>

# Servidor
HOST=0.0.0.0
PORT=8000
DEBUG=False

# 🔥 URL DO SERVIDOR (CRUCIAL PARA PRODUÇÃO!)
SERVER_BASE_URL=https://seudominio.com
# Exemplos:
# SERVER_BASE_URL=https://chat.minhaempresa.com
# SERVER_BASE_URL=https://terminalchat.herokuapp.com
# SERVER_BASE_URL=http://192.168.1.100:8000  # Para rede local

# CORS
CORS_ORIGINS=https://seudominio.com,https://www.seudominio.com
```

### 2. Exemplos de Configuração por Ambiente

#### 🏠 **Desenvolvimento Local**
```bash
SERVER_BASE_URL=http://localhost:8000
```

#### 🌐 **Rede Local/Escritório**
```bash
SERVER_BASE_URL=http://192.168.1.100:8000
# Use o IP do servidor na rede local
```

#### ☁️ **Servidor VPS/Dedicado**
```bash
SERVER_BASE_URL=https://meuservidor.com
# ou
SERVER_BASE_URL=http://45.123.456.789:8000
```

#### 📱 **Heroku**
```bash
SERVER_BASE_URL=https://meu-terminal-chat.herokuapp.com
```

#### 🐳 **Docker/DigitalOcean**
```bash
SERVER_BASE_URL=https://chat.meudominio.com
```

### 3. Configuração de DNS (se usar domínio)

```bash
# Configure seu DNS apontando para o servidor:
chat.seudominio.com -> IP_DO_SERVIDOR

# Exemplo de configuração nginx:
server {
    listen 80;
    server_name chat.seudominio.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. HTTPS em Produção (Recomendado)

```bash
# Use Let's Encrypt para SSL gratuito:
sudo certbot --nginx -d chat.seudominio.com

# Depois altere para:
SERVER_BASE_URL=https://chat.seudominio.com
```

### 5. Variáveis de Ambiente por Plataforma

#### **Linux/macOS**
```bash
export SERVER_BASE_URL="https://meudominio.com"
export SECRET_KEY="chave-super-secreta"
```

#### **Windows**
```cmd
set SERVER_BASE_URL=https://meudominio.com
set SECRET_KEY=chave-super-secreta
```

#### **Docker**
```dockerfile
ENV SERVER_BASE_URL=https://meudominio.com
ENV SECRET_KEY=chave-super-secreta
```

### 6. Teste de Configuração

Para verificar se está funcionando:

1. **Registre um usuário**
2. **Verifique o email recebido**
3. **O link deve apontar para sua URL de produção**

❌ **Errado**: `http://localhost:8000/verify-email?token=...`
✅ **Correto**: `https://seudominio.com/verify-email?token=...`

### 7. Configurações Avançadas

#### **Múltiplos Domínios/Ambientes**
```bash
# .env.production
SERVER_BASE_URL=https://chat.empresa.com

# .env.staging  
SERVER_BASE_URL=https://staging-chat.empresa.com

# .env.development
SERVER_BASE_URL=http://localhost:8000
```

#### **Balanceamento de Carga**
```bash
# Se usar múltiplos servidores
SERVER_BASE_URL=https://chat-api.empresa.com
```

### 8. Checklist de Produção

- [ ] `SECRET_KEY` alterada para valor único e seguro
- [ ] `SERVER_BASE_URL` configurada com URL real
- [ ] Email de produção configurado
- [ ] `DEBUG=False`
- [ ] HTTPS configurado (se possível)
- [ ] Firewall configurado (porta 8000)
- [ ] Backup do banco de dados configurado
- [ ] Monitoramento de logs ativado

### 9. Problemas Comuns

**🔴 Problema**: Usuários não conseguem verificar email
**✅ Solução**: Verifique se `SERVER_BASE_URL` está correto

**🔴 Problema**: Link de verificação dá erro 404
**✅ Solução**: Certifique-se que o servidor está acessível na URL configurada

**🔴 Problema**: Email vai para spam
**✅ Solução**: Configure SPF/DKIM no seu domínio

### 10. Comandos Úteis

```bash
# Verificar configuração atual
grep SERVER_BASE_URL .env

# Testar conectividade
curl https://seudominio.com/docs

# Ver logs do servidor
tail -f /var/log/terminal-chat/server.log
```

---

**💡 Dica**: Sempre teste o fluxo completo de registro → verificação de email → login em um ambiente de staging antes de fazer deploy em produção!