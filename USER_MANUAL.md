# Terminal Chat - User Manual

## Getting Started

### Registration
1. Launch Terminal Chat
2. Select "Register" on the login screen
3. Fill in your details:
   - Username (unique identifier)
   - Email address (for verification)
   - Password (minimum 6 characters)
4. Check your email for verification link
5. Click the verification link to activate your account

### Login
1. Enter your username and password
2. Click "Login"
3. You'll be taken to the main chat interface

## Main Interface

The Terminal Chat interface consists of two main areas:

### Left Sidebar - Chat Rooms
- 💬 **Chat Rooms**: List of available rooms
- Click on any room name to join
- **Refresh Rooms**: Updates the room list

### Right Side - Chat Area
- **Chat Title**: Shows current room name
- **Messages Area**: Displays chat history and live messages
- **Input Area**: Type and send messages

## Chat Features

### Text Messaging
1. **Join a Room**: Click on a room name in the sidebar
2. **Send Messages**: Type in the input field and press Enter or click Send
3. **View History**: Previous messages load automatically when joining a room

### Real-time Features
- Messages appear instantly for all users in the room
- See when users join or leave rooms
- Timestamps show when messages were sent

### Voice Chat (Beta)
- **Start Voice**: Press `Ctrl+V` while in a room
- **Stop Voice**: Press `Ctrl+V` again to stop
- **Mute/Unmute**: Press `Ctrl+M` to toggle microphone
- Voice chat works alongside text chat

## Keyboard Shortcuts

### Global Shortcuts
- `Ctrl+Q`: Quit application
- `Tab`: Navigate between interface elements
- `Enter`: Send message (when in input field)

### Chat Shortcuts
- `Ctrl+V`: Toggle voice chat
- `Ctrl+M`: Toggle microphone mute
- `Ctrl+R`: Refresh room list
- `Page Up/Down`: Scroll through message history

### Navigation
- `↑/↓`: Navigate room list
- `Ctrl+1-9`: Quick switch to room number
- `Esc`: Return to previous screen

## Room Management

### Joining Rooms
- **General Room**: Default room all users can access
- **Public Rooms**: Visible to all users
- **Private Rooms**: Require invitation (future feature)

### Room Features
- **Persistent History**: Messages are saved and loaded when rejoining
- **User Notifications**: See when others join/leave
- **Room Descriptions**: Hover over room names for details

## Account Management

### Profile Settings
- Currently managed through registration
- Future updates will include profile editing

### Password Reset
- Contact administrator or re-register if password is forgotten
- Password reset feature coming in future updates

## Voice Chat Guide

### Setup Requirements
- Working microphone and speakers/headphones
- Adequate internet connection
- Audio permissions granted to the application

### Using Voice Chat
1. **Join a Text Chat Room First**
2. **Start Voice**: Use `Ctrl+V` or voice menu
3. **Talk Naturally**: Your voice is transmitted in real-time
4. **Listen**: Hear other users' voices automatically
5. **Stop When Done**: Turn off voice to save bandwidth

### Voice Quality Tips
- Use headphones to prevent echo
- Speak clearly and at normal volume
- Mute when not speaking in busy rooms
- Check microphone levels if others can't hear you

### Troubleshooting Voice
- **Can't Hear Others**: Check speakers/headphones
- **Others Can't Hear You**: Check microphone permissions
- **Echo Issues**: Use headphones instead of speakers
- **Connection Issues**: Restart voice chat or rejoin room

## Privacy and Security

### What's Encrypted
- Passwords (hashed with bcrypt)
- Authentication tokens
- WebSocket connections can be secured with WSS

### What's Stored
- User accounts and profiles
- Chat message history
- Room membership information
- Voice chat is real-time only (not recorded)

### Privacy Tips
- Use a unique username (don't use real name if privacy is a concern)
- Be aware that messages are stored on the server
- Voice conversations are not recorded
- Administrators can see message history

## Troubleshooting

### Connection Issues
1. **Can't Connect to Server**:
   - Check internet connection
   - Verify server is running
   - Check firewall settings

2. **Messages Not Sending**:
   - Check connection status
   - Try rejoining the room
   - Restart the application

3. **Can't Join Rooms**:
   - Ensure you're logged in
   - Check if room still exists
   - Try refreshing room list

### Audio Issues
1. **No Sound**:
   - Check system audio settings
   - Verify speakers/headphones are working
   - Grant microphone permissions

2. **Microphone Not Working**:
   - Check system microphone settings
   - Grant application permissions
   - Test microphone in other applications

3. **Voice Chat Won't Start**:
   - Ensure you're in a chat room
   - Check audio device availability
   - Restart application if needed

### Performance Issues
1. **Application Slow**:
   - Close unnecessary applications
   - Check available memory
   - Restart Terminal Chat

2. **High CPU Usage**:
   - Turn off voice chat when not needed
   - Limit number of active rooms
   - Update to latest version

### Getting Help
1. Check this manual for solutions
2. Review setup documentation
3. Check server status and logs
4. Contact system administrator

## Advanced Features

### Command Line Options
```bash
terminal-chat --server=custom-server.com:8000  # Custom server
terminal-chat --debug                          # Debug mode
terminal-chat --config=/path/to/config        # Custom config
```

### Configuration Files
- Client settings: `~/.terminal-chat/config`
- Logs: `~/.terminal-chat/logs/`
- Cache: `~/.terminal-chat/cache/`

## Tips for Best Experience

### General Usage
- Keep messages concise and clear
- Use proper spelling and grammar
- Be respectful to other users
- Don't spam or flood chat rooms

### Voice Chat Etiquette
- Announce when joining voice chat
- Mute when eating, typing, or in noisy environments
- Keep conversations relevant to the room topic
- Be patient with audio delays

### Performance Optimization
- Close voice chat when not actively using it
- Clear message history periodically (future feature)
- Use wired internet connection for best voice quality
- Keep the application updated

## Upcoming Features

### Planned Additions
- Private messaging between users
- File sharing capabilities
- Custom room creation
- Advanced user profiles
- Message search functionality
- Mobile companion app

### Voice Chat Improvements
- Better audio quality
- Noise cancellation
- Push-to-talk mode
- Voice recording (optional)
- Multiple audio channels

Stay tuned for updates!