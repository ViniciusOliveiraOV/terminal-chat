# Terminal Chat - Setup Guide

## Prerequisites

- Python 3.8 or higher
- Audio device (microphone and speakers) for voice chat
- Internet connection

## Server Setup

1. **Navigate to the server directory:**
   ```bash
   cd server
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your settings:
   - `SECRET_KEY`: Change to a secure random string
   - `EMAIL_USERNAME` & `EMAIL_PASSWORD`: Gmail credentials for email verification
   - Other settings as needed

4. **Start the server:**
   ```bash
   python main.py
   ```
   
   The server will be available at `http://localhost:8000`

## Client Setup (Development)

1. **Navigate to the client directory:**
   ```bash
   cd client
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure client settings (optional):**
   ```bash
   cp .env.example .env
   ```

4. **Run the client:**
   ```bash
   python main.py
   ```

## Building Standalone Executables

To create standalone executables that don't require Python installation:

1. **From the project root:**
   ```bash
   python build.py
   ```

2. **Install the application:**
   
   **Windows:**
   ```cmd
   # Run as Administrator
   install.bat
   ```
   
   **Linux:**
   ```bash
   ./install.sh
   ```

3. **Run Terminal Chat:**
   ```bash
   terminal-chat
   ```

## Email Configuration

For user registration and email verification, you need to configure email settings:

### Gmail Setup
1. Enable 2-factor authentication on your Gmail account
2. Generate an "App Password" for Terminal Chat
3. Use your Gmail address as `EMAIL_USERNAME`
4. Use the app password as `EMAIL_PASSWORD`

### Other Email Providers
Update the SMTP settings in your `.env` file:
- `SMTP_SERVER`: Your email provider's SMTP server
- `SMTP_PORT`: Usually 587 for TLS or 465 for SSL
- `EMAIL_USERNAME` & `EMAIL_PASSWORD`: Your email credentials

## Firewall Configuration

If users can't connect, ensure these ports are open:
- **8000**: HTTP/WebSocket server
- **3478**: STUN server for voice chat (optional)

## Troubleshooting

### Common Issues

1. **"Import could not be resolved" errors:**
   - Make sure all dependencies are installed
   - Use a virtual environment to avoid conflicts

2. **Voice chat not working:**
   - Ensure microphone permissions are granted
   - Check that PyAudio is properly installed
   - On Linux, you may need to install additional audio libraries

3. **Email verification not working:**
   - Verify SMTP credentials in `.env`
   - Check spam folder for verification emails
   - Ensure "Less secure app access" is enabled (for Gmail)

4. **WebSocket connection fails:**
   - Check if server is running on correct port
   - Verify firewall settings
   - Ensure no proxy is blocking WebSocket connections

### Platform-Specific Issues

**Windows:**
- Install Microsoft Visual C++ Redistributable if audio doesn't work
- Run as Administrator if installation fails

**Linux:**
- Install audio development libraries:
  ```bash
  sudo apt-get install portaudio19-dev python3-pyaudio
  ```
- For some distributions, you may need additional packages:
  ```bash
  sudo apt-get install build-essential libffi-dev libssl-dev
  ```

## Development Mode

For development and testing:

1. **Start server in debug mode:**
   ```bash
   cd server
   DEBUG=True python main.py
   ```

2. **Run client with auto-reload:**
   ```bash
   cd client
   python main.py --dev
   ```

## Network Deployment

To deploy on a network:

1. **Update server configuration:**
   - Set `HOST=0.0.0.0` in server settings
   - Configure firewall to allow port 8000

2. **Update client configuration:**
   - Change `SERVER_URL` to your server's IP address
   - Update `WEBSOCKET_URL` accordingly

3. **Use reverse proxy (recommended for production):**
   Set up nginx or Apache to proxy requests to the Python server

## Security Notes

- Change the default `SECRET_KEY` in production
- Use HTTPS in production environments
- Regularly update dependencies for security patches
- Consider implementing rate limiting for production use