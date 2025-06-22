import whisper
import os

class MeetingTranscriber:
    def __init__(self, model_size="base"):
        """Initialize Whisper model for transcription"""
        print(f"📥 Loading Whisper {model_size} model...")
        self.model = whisper.load_model(model_size)
        print("✅ Transcription model loaded!")
    
    def transcribe_audio(self, audio_file):
        """Transcribe audio file to text"""
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        
        print("🔄 Transcribing audio... This may take a few minutes.")
        
        try:
            # Transcribe the audio
            result = self.model.transcribe(audio_file)
            transcript = result["text"]
            
            print("✅ Transcription completed!")
            return transcript.strip()
            
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            return ""
    
    def transcribe_with_timestamps(self, audio_file):
        """Transcribe with timestamps for each segment"""
        result = self.model.transcribe(audio_file)
        return result["segments"]  # Returns list with timestamps
