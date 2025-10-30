# Terminal Chat Application

A cross-platform terminal-based chat application with real-time messaging and voice chat capabilities.

## Features

- 🔐 User registration and authentication with email confirmation
- 💬 Real-time text messaging in chat rooms
- 🎤 Real-time voice chat without calling
- 🖥️ Cross-platform support (Windows & Linux)
- 🌑 Minimalist black terminal interface
- 🔒 Secure communication with encrypted messages

## Architecture

- **Client**: Terminal-based application built with Python and Textual
- **Server**: FastAPI backend with WebSocket support
- **Database**: SQLite with SQLAlchemy ORM
- **Voice**: WebRTC implementation for real-time audio

## Quick Start

### Server Setup
```bash
cd server
cp .env.example .env
# Edit .env with your settings (especially SERVER_BASE_URL for production!)
pip install -r requirements.txt
python main.py
```

### Client Setup
```bash
cd client
pip install -r requirements.txt
python main.py
```

### ⚠️ Production Configuration
**IMPORTANT**: For production deployment, you MUST update `SERVER_BASE_URL` in your `.env` file:

```bash
# Development
SERVER_BASE_URL=http://localhost:8000

# Production
SERVER_BASE_URL=https://yourdomain.com
```

See [PRODUCTION.md](PRODUCTION.md) for detailed production setup guide.

## Build Standalone Executables

```bash
# For current platform
python build.py

# The executable will be created in the dist/ directory
```

## System Requirements

- Python 3.8+
- Audio device for voice chat
- Internet connection for server communication

## License

MIT License