import pyaudio
import wave
import threading
import time

class MeetingRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.recording = False
        self.frames = []
    
    def start_recording(self, filename="meeting_audio.wav"):
        """Start recording audio from microphone"""
        self.recording = True
        self.frames = []
        
        # Configure audio stream
        stream = self.audio.open(
            format=pyaudio.paInt16,    # 16-bit audio
            channels=1,                # Mono recording
            rate=44100,               # Sample rate
            input=True,               # Input stream
            frames_per_buffer=1024    # Buffer size
        )
        
        print("🎤 Recording started... Press Enter to stop.")
        
        # Record audio in chunks
        while self.recording:
            try:
                data = stream.read(1024, exception_on_overflow=False)
                self.frames.append(data)
            except Exception as e:
                print(f"Recording error: {e}")
                break
        
        # Clean up
        stream.stop_stream()
        stream.close()
        
        # Save recording to file
        self.save_recording(filename)
        print(f"✅ Recording saved as {filename}")
    
    def save_recording(self, filename):
        """Save recorded frames to WAV file"""
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))
    
    def stop_recording(self):
        """Stop the recording"""
        self.recording = False
    
    def __del__(self):
        """Clean up audio resources"""
        if hasattr(self, 'audio'):
            self.audio.terminate()
