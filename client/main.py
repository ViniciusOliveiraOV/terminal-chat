from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Input, Static, ListView, ListItem, Button, Label
from textual.reactive import reactive
from textual import events
from textual.screen import Screen
from rich.text import Text
from rich.console import Console
import asyncio
from datetime import datetime
from chat_client import ChatClient, Config

class LoginScreen(Screen):
    """Login/Register screen"""
    
    def compose(self) -> ComposeResult:
        yield Container(
            Static("🔥 Terminal Chat", classes="title"),
            Static("Welcome to the minimalist chat experience", classes="subtitle"),
            Container(
                Label("Username:"),
                Input(placeholder="Enter username", id="username"),
                Label("Password:"),
                Input(placeholder="Enter password", password=True, id="password"),
                Horizontal(
                    Button("Login", id="login", variant="primary"),
                    Button("Register", id="register"),
                ),
                classes="login-form"
            ),
            classes="login-container"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "login":
            self.handle_login()
        elif event.button.id == "register":
            self.app.push_screen("register")
    
    def handle_login(self):
        username_input = self.query_one("#username", Input)
        password_input = self.query_one("#password", Input)
        
        username = username_input.value.strip()
        password = password_input.value.strip()
        
        if not username or not password:
            self.notify("Please enter both username and password", severity="error")
            return
        
        # Attempt login
        result = self.app.client.login(username, password)
        if result["success"]:
            self.notify(f"Welcome back, {username}!", severity="information")
            self.app.switch_screen("main")
        else:
            error_msg = result.get("error", {}).get("detail", "Login failed")
            self.notify(error_msg, severity="error")

class RegisterScreen(Screen):
    """Registration screen"""
    
    def compose(self) -> ComposeResult:
        yield Container(
            Static("📝 Create Account", classes="title"),
            Container(
                Label("Username:"),
                Input(placeholder="Choose a username", id="reg_username"),
                Label("Email:"),
                Input(placeholder="your@email.com", id="reg_email"),
                Label("Password:"),
                Input(placeholder="Choose a strong password", password=True, id="reg_password"),
                Label("Confirm Password:"),
                Input(placeholder="Confirm your password", password=True, id="reg_confirm"),
                Horizontal(
                    Button("Create Account", id="create_account", variant="primary"),
                    Button("Back to Login", id="back_login"),
                ),
                classes="register-form"
            ),
            classes="register-container"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "create_account":
            self.handle_register()
        elif event.button.id == "back_login":
            self.app.pop_screen()
    
    def handle_register(self):
        username = self.query_one("#reg_username", Input).value.strip()
        email = self.query_one("#reg_email", Input).value.strip()
        password = self.query_one("#reg_password", Input).value.strip()
        confirm = self.query_one("#reg_confirm", Input).value.strip()
        
        if not all([username, email, password, confirm]):
            self.notify("Please fill in all fields", severity="error")
            return
        
        if password != confirm:
            self.notify("Passwords do not match", severity="error")
            return
        
        if len(password) < 6:
            self.notify("Password must be at least 6 characters", severity="error")
            return
        
        # Attempt registration
        result = self.app.client.register(username, email, password)
        if result["success"]:
            self.notify("Account created! Please check your email to verify your account.", severity="information")
            self.app.pop_screen()
        else:
            error_msg = result.get("error", {}).get("detail", "Registration failed")
            self.notify(error_msg, severity="error")

class MainChatScreen(Screen):
    """Main chat interface"""
    
    current_room = reactive(None)
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Horizontal(
                # Room list sidebar
                Container(
                    Static("💬 Chat Rooms", classes="sidebar-title"),
                    ListView(id="rooms_list"),
                    Button("Refresh Rooms", id="refresh_rooms"),
                    classes="sidebar"
                ),
                # Chat area
                Container(
                    Static("Select a room to start chatting", id="chat_title", classes="chat-title"),
                    Container(id="messages_container", classes="messages"),
                    Horizontal(
                        Input(placeholder="Type your message...", id="message_input", classes="message-input"),
                        Button("Send", id="send_message", variant="primary"),
                        classes="input-area"
                    ),
                    classes="chat-area"
                )
            )
        )
        yield Footer()
    
    def on_mount(self) -> None:
        self.load_rooms()
    
    def load_rooms(self):
        """Load available chat rooms"""
        result = self.app.client.get_rooms()
        if result["success"]:
            rooms_list = self.query_one("#rooms_list", ListView)
            rooms_list.clear()
            
            for room in result["data"]:
                item = ListItem(
                    Label(f"#{room['name']}"),
                    classes="room-item"
                )
                item.room_data = room
                rooms_list.append(item)
        else:
            self.notify("Failed to load rooms", severity="error")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "refresh_rooms":
            self.load_rooms()
        elif event.button.id == "send_message":
            self.send_message()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "message_input":
            self.send_message()
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.list_view.id == "rooms_list":
            room_data = event.item.room_data
            self.join_room(room_data)
    
    async def join_room(self, room_data):
        """Join a chat room"""
        room_id = room_data["id"]
        room_name = room_data["name"]
        
        # Join room on server
        result = self.app.client.join_room(room_id)
        if not result["success"]:
            self.notify("Failed to join room", severity="error")
            return
        
        # Update UI
        chat_title = self.query_one("#chat_title", Static)
        chat_title.update(f"💬 #{room_name}")
        
        # Load message history
        self.load_messages(room_id)
        
        # Connect WebSocket
        try:
            await self.app.client.connect_websocket(room_id)
            self.current_room = room_id
            
            # Start listening for messages
            asyncio.create_task(self.listen_for_messages())
            
        except Exception as e:
            self.notify(f"Failed to connect to room: {e}", severity="error")
    
    def load_messages(self, room_id):
        """Load chat history"""
        result = self.app.client.get_messages(room_id)
        if result["success"]:
            messages_container = self.query_one("#messages_container", Container)
            messages_container.remove_children()
            
            for msg in result["data"]:
                timestamp = datetime.fromisoformat(msg["timestamp"].replace("Z", "+00:00"))
                time_str = timestamp.strftime("%H:%M")
                
                message_widget = Static(
                    f"[dim]{time_str}[/] [bold cyan]{msg['username']}[/]: {msg['content']}",
                    classes="message"
                )
                messages_container.mount(message_widget)
    
    async def send_message(self):
        """Send a message"""
        if not self.current_room:
            self.notify("Please join a room first", severity="warning")
            return
        
        message_input = self.query_one("#message_input", Input)
        content = message_input.value.strip()
        
        if not content:
            return
        
        try:
            await self.app.client.send_message(content)
            message_input.value = ""
        except Exception as e:
            self.notify(f"Failed to send message: {e}", severity="error")
    
    async def listen_for_messages(self):
        """Listen for incoming messages"""
        try:
            await self.app.client.listen_messages(self.handle_incoming_message)
        except Exception as e:
            self.notify(f"Connection lost: {e}", severity="error")
    
    def handle_incoming_message(self, data):
        """Handle incoming WebSocket message"""
        if data["type"] == "chat_message":
            timestamp = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
            time_str = timestamp.strftime("%H:%M")
            
            messages_container = self.query_one("#messages_container", Container)
            message_widget = Static(
                f"[dim]{time_str}[/] [bold cyan]{data['username']}[/]: {data['content']}",
                classes="message"
            )
            messages_container.mount(message_widget)
            
            # Auto-scroll to bottom
            messages_container.scroll_end()
        
        elif data["type"] in ["user_joined", "user_left"]:
            messages_container = self.query_one("#messages_container", Container)
            timestamp = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
            time_str = timestamp.strftime("%H:%M")
            
            system_message = Static(
                f"[dim]{time_str} {data['message']}[/]",
                classes="system-message"
            )
            messages_container.mount(system_message)

class TerminalChatApp(App):
    """Main application"""
    
    CSS = """
    .title {
        text-align: center;
        text-style: bold;
        color: #00ff41;
        margin: 1;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2;
    }
    
    .login-container, .register-container {
        align: center middle;
        width: 60;
        height: auto;
        background: #111;
        border: solid #333;
    }
    
    .login-form, .register-form {
        padding: 2;
        height: auto;
    }
    
    .sidebar {
        width: 25%;
        height: 100%;
        background: #111;
        border-right: solid #333;
        padding: 1;
    }
    
    .sidebar-title {
        text-style: bold;
        color: #00ff41;
        margin-bottom: 1;
    }
    
    .chat-area {
        width: 75%;
        height: 100%;
        background: #000;
    }
    
    .chat-title {
        height: 3;
        text-style: bold;
        color: #00ff41;
        background: #111;
        padding-left: 2;
        border-bottom: solid #333;
    }
    
    .messages {
        height: 1fr;
        overflow-y: auto;
        padding: 1;
        background: #000;
    }
    
    .message {
        margin-bottom: 1;
        color: #fff;
    }
    
    .system-message {
        margin-bottom: 1;
        color: #666;
        text-style: italic;
    }
    
    .input-area {
        height: 3;
        background: #111;
        border-top: solid #333;
    }
    
    .message-input {
        width: 1fr;
        margin: 1;
    }
    
    .room-item {
        color: #00ff41;
        margin-bottom: 1;
    }
    
    .room-item:hover {
        background: #333;
    }
    
    Button {
        margin: 1;
    }
    
    Label {
        margin-bottom: 1;
        color: #fff;
    }
    
    Input {
        margin-bottom: 1;
    }
    """
    
    SCREENS = {
        "login": LoginScreen,
        "register": RegisterScreen,
        "main": MainChatScreen,
    }
    
    def __init__(self):
        super().__init__()
        self.client = ChatClient(Config())
    
    def on_mount(self) -> None:
        self.push_screen("login")

if __name__ == "__main__":
    app = TerminalChatApp()
    app.run()