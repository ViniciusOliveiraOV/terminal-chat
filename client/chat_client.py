import requests
import json
import asyncio
import websockets
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class Config:
    server_url: str = "http://localhost:8000"
    websocket_url: str = "ws://localhost:8000"

class ChatClient:
    def __init__(self, config: Config):
        self.config = config
        self.token: Optional[str] = None
        self.username: Optional[str] = None
        self.websocket: Optional[websockets.WebSocketServerProtocol] = None
        self.current_room_id: Optional[int] = None
        
    def register(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Register a new user"""
        try:
            response = requests.post(
                f"{self.config.server_url}/register",
                json={
                    "username": username,
                    "email": email,
                    "password": password
                }
            )
            return {"success": response.status_code == 200, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Login user and get token"""
        try:
            response = requests.post(
                f"{self.config.server_url}/login",
                json={
                    "username": username,
                    "password": password
                }
            )
            if response.status_code == 200:
                data = response.json()
                self.token = data["access_token"]
                self.username = username
                return {"success": True, "data": data}
            else:
                return {"success": False, "error": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_rooms(self) -> Dict[str, Any]:
        """Get available chat rooms"""
        if not self.token:
            return {"success": False, "error": "Not authenticated"}
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.config.server_url}/rooms", headers=headers)
            return {"success": response.status_code == 200, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def join_room(self, room_id: int) -> Dict[str, Any]:
        """Join a chat room"""
        if not self.token:
            return {"success": False, "error": "Not authenticated"}
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(
                f"{self.config.server_url}/rooms/{room_id}/join",
                headers=headers
            )
            return {"success": response.status_code == 200, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_messages(self, room_id: int, limit: int = 50) -> Dict[str, Any]:
        """Get chat history for a room"""
        if not self.token:
            return {"success": False, "error": "Not authenticated"}
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(
                f"{self.config.server_url}/rooms/{room_id}/messages?limit={limit}",
                headers=headers
            )
            return {"success": response.status_code == 200, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def connect_websocket(self, room_id: int):
        """Connect to WebSocket for real-time chat"""
        if not self.token:
            raise Exception("Not authenticated")
        
        ws_url = f"{self.config.websocket_url}/ws/{room_id}?token={self.token}"
        self.websocket = await websockets.connect(ws_url)
        self.current_room_id = room_id
    
    async def send_message(self, content: str):
        """Send a message through WebSocket"""
        if not self.websocket:
            raise Exception("WebSocket not connected")
        
        message = {
            "type": "chat_message",
            "content": content
        }
        await self.websocket.send(json.dumps(message))
    
    async def listen_messages(self, callback):
        """Listen for incoming messages"""
        if not self.websocket:
            raise Exception("WebSocket not connected")
        
        try:
            async for message in self.websocket:
                data = json.loads(message)
                callback(data)
        except websockets.exceptions.ConnectionClosed:
            pass
    
    async def disconnect(self):
        """Disconnect from WebSocket"""
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
            self.current_room_id = None