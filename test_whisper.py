import whisper
import os

model = whisper.load_model("base")
audio_path = r"C:\Users\Abhishek\OneDrive\Desktop\meeting-assistant\meeting_20250622_155056.wav"

print("📁 File exists:", os.path.exists(audio_path))

try:
    result = model.transcribe(audio_path)
    print("✅ Transcription success:")
    print(result['text'])
except Exception as e:
    print("❌ Transcription error:", e)
