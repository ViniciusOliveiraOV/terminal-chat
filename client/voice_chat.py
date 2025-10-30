import asyncio
import json
import pyaudio
import threading
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
from aiortc.contrib.media import MediaRecorder, MediaPlayer
import logging

# Configure logging for aiortc
logging.basicConfig(level=logging.INFO)

class AudioTrack(MediaStreamTrack):
    """Custom audio track for capturing microphone input"""
    
    kind = "audio"
    
    def __init__(self):
        super().__init__()
        
        # Audio configuration
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.chunk = 1024
        
        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.running = False
        
    def start_recording(self):
        """Start recording audio from microphone"""
        try:
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            self.running = True
        except Exception as e:
            print(f"Failed to start audio recording: {e}")
    
    def stop_recording(self):
        """Stop recording audio"""
        self.running = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
    
    async def recv(self):
        """Receive audio frame"""
        if not self.running or not self.stream:
            return None
        
        try:
            # Read audio data from microphone
            data = self.stream.read(self.chunk, exception_on_overflow=False)
            # Convert to appropriate format for WebRTC
            # This is a simplified implementation
            return data
        except Exception as e:
            print(f"Error reading audio: {e}")
            return None

class VoiceChatManager:
    """Manages voice chat functionality using WebRTC"""
    
    def __init__(self, websocket_client):
        self.websocket = websocket_client
        self.pc = None  # RTCPeerConnection
        self.audio_track = None
        self.is_voice_active = False
        self.current_room_id = None
        
        # Audio playback
        self.audio = pyaudio.PyAudio()
        self.playback_stream = None
        
    async def start_voice_chat(self, room_id: int):
        """Start voice chat in a room"""
        if self.is_voice_active:
            return {"success": False, "error": "Voice chat already active"}
        
        try:
            # Create RTCPeerConnection
            self.pc = RTCPeerConnection()
            self.current_room_id = room_id
            
            # Create audio track
            self.audio_track = AudioTrack()
            self.audio_track.start_recording()
            
            # Add audio track to peer connection
            self.pc.addTrack(self.audio_track)
            
            # Set up event handlers
            self.pc.on("track", self.on_track)
            self.pc.on("icecandidate", self.on_ice_candidate)
            
            # Create offer
            offer = await self.pc.createOffer()
            await self.pc.setLocalDescription(offer)
            
            # Send offer through WebSocket
            await self.websocket.send(json.dumps({
                "type": "voice_offer",
                "room_id": room_id,
                "offer": {
                    "type": offer.type,
                    "sdp": offer.sdp
                }
            }))
            
            self.is_voice_active = True
            return {"success": True, "message": "Voice chat started"}
            
        except Exception as e:
            return {"success": False, "error": f"Failed to start voice chat: {e}"}
    
    async def stop_voice_chat(self):
        """Stop voice chat"""
        if not self.is_voice_active:
            return
        
        try:
            # Stop audio recording
            if self.audio_track:
                self.audio_track.stop_recording()
                self.audio_track = None
            
            # Stop audio playback
            if self.playback_stream:
                self.playback_stream.stop_stream()
                self.playback_stream.close()
                self.playback_stream = None
            
            # Close peer connection
            if self.pc:
                await self.pc.close()
                self.pc = None
            
            # Notify others in room
            if self.current_room_id:
                await self.websocket.send(json.dumps({
                    "type": "voice_stop",
                    "room_id": self.current_room_id
                }))
            
            self.is_voice_active = False
            self.current_room_id = None
            
        except Exception as e:
            print(f"Error stopping voice chat: {e}")
    
    async def handle_voice_offer(self, offer_data):
        """Handle incoming voice offer"""
        try:
            if not self.pc:
                self.pc = RTCPeerConnection()
                self.pc.on("track", self.on_track)
            
            # Set remote description
            offer = RTCSessionDescription(
                sdp=offer_data["offer"]["sdp"],
                type=offer_data["offer"]["type"]
            )
            await self.pc.setRemoteDescription(offer)
            
            # Create and send answer
            answer = await self.pc.createAnswer()
            await self.pc.setLocalDescription(answer)
            
            await self.websocket.send(json.dumps({
                "type": "voice_answer",
                "room_id": offer_data["room_id"],
                "answer": {
                    "type": answer.type,
                    "sdp": answer.sdp
                }
            }))
            
        except Exception as e:
            print(f"Error handling voice offer: {e}")
    
    async def handle_voice_answer(self, answer_data):
        """Handle incoming voice answer"""
        try:
            if self.pc:
                answer = RTCSessionDescription(
                    sdp=answer_data["answer"]["sdp"],
                    type=answer_data["answer"]["type"]
                )
                await self.pc.setRemoteDescription(answer)
        except Exception as e:
            print(f"Error handling voice answer: {e}")
    
    def on_track(self, track):
        """Handle incoming audio track"""
        if track.kind == "audio":
            # Set up audio playback
            def play_audio():
                try:
                    self.playback_stream = self.audio.open(
                        format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        output=True,
                        frames_per_buffer=1024
                    )
                    
                    # This is a simplified audio playback loop
                    # In a real implementation, you'd need proper audio format conversion
                    while self.is_voice_active and self.playback_stream:
                        # Receive audio data and play it
                        # This would need proper implementation with aiortc
                        pass
                        
                except Exception as e:
                    print(f"Audio playback error: {e}")
            
            threading.Thread(target=play_audio, daemon=True).start()
    
    def on_ice_candidate(self, candidate):
        """Handle ICE candidates"""
        # In a full implementation, you'd exchange ICE candidates
        # through the signaling server (WebSocket)
        pass
    
    def toggle_mute(self):
        """Toggle microphone mute"""
        if self.audio_track and self.is_voice_active:
            # Implementation would toggle the audio track
            pass
    
    def get_voice_status(self):
        """Get current voice chat status"""
        return {
            "active": self.is_voice_active,
            "room_id": self.current_room_id,
            "muted": False  # Would track mute state
        }