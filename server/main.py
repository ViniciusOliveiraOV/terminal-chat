from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
import json
import asyncio
from datetime import datetime, timedelta

from database import create_tables, get_db, User, ChatRoom, Message, RoomMembership
from auth import AuthService
from pydantic import BaseModel, EmailStr

# Pydantic models for API
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class CreateRoom(BaseModel):
    name: str
    description: Optional[str] = None
    is_private: bool = False

class SendMessage(BaseModel):
    content: str
    room_id: int

class Token(BaseModel):
    access_token: str
    token_type: str

# FastAPI app
app = FastAPI(title="Terminal Chat Server", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}
        self.user_connections: Dict[int, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int, room_id: int):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)
        self.user_connections[user_id] = websocket
    
    def disconnect(self, websocket: WebSocket, user_id: int, room_id: int):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
        if user_id in self.user_connections:
            del self.user_connections[user_id]
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast_to_room(self, message: str, room_id: int):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                try:
                    await connection.send_text(message)
                except:
                    # Remove dead connections
                    self.active_connections[room_id].remove(connection)

manager = ConnectionManager()

# Dependency to get current user from token
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    user = AuthService.get_current_user(db, token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not verified",
        )
    return user

# Initialize database
@app.on_event("startup")
async def startup_event():
    create_tables()
    
    # Create default general room
    db = next(get_db())
    general_room = db.query(ChatRoom).filter(ChatRoom.name == "general").first()
    if not general_room:
        general_room = ChatRoom(
            name="general",
            description="General chat room for everyone",
            is_private=False
        )
        db.add(general_room)
        db.commit()

# Authentication endpoints
@app.post("/register", response_model=dict)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    user = AuthService.register_user(db, user_data.username, user_data.email, user_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    return {"message": "User registered successfully. Please check your email to verify your account."}

@app.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please verify your email before logging in",
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = AuthService.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/verify-email")
async def verify_email(token: str, db: Session = Depends(get_db)):
    if AuthService.verify_email(db, token):
        return {"message": "Email verified successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification token"
        )

# Chat room endpoints
@app.get("/rooms")
async def get_rooms(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rooms = db.query(ChatRoom).all()
    return [{"id": room.id, "name": room.name, "description": room.description} for room in rooms]

@app.post("/rooms")
async def create_room(room_data: CreateRoom, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    room = ChatRoom(
        name=room_data.name,
        description=room_data.description,
        is_private=room_data.is_private,
        created_by=current_user.id
    )
    db.add(room)
    db.commit()
    db.refresh(room)
    
    # Add creator as admin member
    membership = RoomMembership(
        user_id=current_user.id,
        room_id=room.id,
        is_admin=True
    )
    db.add(membership)
    db.commit()
    
    return {"id": room.id, "name": room.name, "description": room.description}

@app.post("/rooms/{room_id}/join")
async def join_room(room_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if room exists
    room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Check if already a member
    membership = db.query(RoomMembership).filter(
        RoomMembership.user_id == current_user.id,
        RoomMembership.room_id == room_id
    ).first()
    
    if membership:
        return {"message": "Already a member of this room"}
    
    # Add membership
    membership = RoomMembership(
        user_id=current_user.id,
        room_id=room_id
    )
    db.add(membership)
    db.commit()
    
    return {"message": "Successfully joined room"}

# WebSocket endpoint for real-time chat
@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, token: str, db: Session = Depends(get_db)):
    # Verify user token
    user = AuthService.get_current_user(db, token)
    if not user or not user.is_verified:
        await websocket.close(code=4001)
        return
    
    # Check if user is member of room
    membership = db.query(RoomMembership).filter(
        RoomMembership.user_id == user.id,
        RoomMembership.room_id == room_id
    ).first()
    
    if not membership:
        await websocket.close(code=4003)
        return
    
    await manager.connect(websocket, user.id, room_id)
    
    # Notify room about user joining
    join_message = {
        "type": "user_joined",
        "username": user.username,
        "message": f"{user.username} joined the room",
        "timestamp": datetime.now().isoformat()
    }
    await manager.broadcast_to_room(json.dumps(join_message), room_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data["type"] == "chat_message":
                # Save message to database
                message = Message(
                    content=message_data["content"],
                    user_id=user.id,
                    room_id=room_id,
                    message_type="text"
                )
                db.add(message)
                db.commit()
                
                # Broadcast to room
                broadcast_message = {
                    "type": "chat_message",
                    "username": user.username,
                    "content": message_data["content"],
                    "timestamp": datetime.now().isoformat()
                }
                await manager.broadcast_to_room(json.dumps(broadcast_message), room_id)
                
            elif message_data["type"] == "voice_offer" or message_data["type"] == "voice_answer":
                # Handle WebRTC signaling for voice chat
                target_user = message_data.get("target_user")
                if target_user and target_user in manager.user_connections:
                    await manager.send_personal_message(data, manager.user_connections[target_user])
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, user.id, room_id)
        # Notify room about user leaving
        leave_message = {
            "type": "user_left",
            "username": user.username,
            "message": f"{user.username} left the room",
            "timestamp": datetime.now().isoformat()
        }
        await manager.broadcast_to_room(json.dumps(leave_message), room_id)

# Get chat history
@app.get("/rooms/{room_id}/messages")
async def get_messages(room_id: int, limit: int = 50, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if user is member of room
    membership = db.query(RoomMembership).filter(
        RoomMembership.user_id == current_user.id,
        RoomMembership.room_id == room_id
    ).first()
    
    if not membership:
        raise HTTPException(status_code=403, detail="Not a member of this room")
    
    messages = db.query(Message).filter(Message.room_id == room_id).order_by(Message.timestamp.desc()).limit(limit).all()
    messages.reverse()  # Show oldest first
    
    return [
        {
            "id": msg.id,
            "content": msg.content,
            "username": msg.user.username,
            "timestamp": msg.timestamp.isoformat(),
            "message_type": msg.message_type
        }
        for msg in messages
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)