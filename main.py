#!/usr/bin/env python3
"""
Meeting Note Taker & Summarizer
Main application file
"""

import threading
import os
import sys
from datetime import datetime

# Import our custom modules
from meeting_recorder import MeetingRecorder
from meeting_transcriber import MeetingTranscriber
from meeting_summarizer import MeetingSummarizer
from email_sender import EmailSender

def main():
    print("🎯 Meeting Note Taker & Summarizer")
    print("=" * 50)
    
    # Initialize components
    print("🚀 Initializing components...")
    recorder = MeetingRecorder()
    transcriber = MeetingTranscriber()
    summarizer = MeetingSummarizer()
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_filename = f"meeting_{timestamp}.wav"
    
    print(f"\n📁 Audio will be saved as: {audio_filename}")
    print("\n" + "="*50)
    
    # Start recording
    print("🎙️  RECORDING PHASE")
    print("Press ENTER to start recording...")
    input()
    
    print("🔴 Starting recording...")
    
    # Start recording in a separate thread
    recording_thread = threading.Thread(
        target=recorder.start_recording,
        args=(audio_filename,)
    )
    recording_thread.start()
    
    # Wait for user to stop recording
    print("Press ENTER to stop recording...")
    input()
    
    # Stop recording
    recorder.stop_recording()
    recording_thread.join()
    
    # Check if audio file was created
    if not os.path.exists(audio_filename):
        print("❌ Error: Audio file was not created!")
        return
    
    print(f"\n📊 Audio file size: {os.path.getsize(audio_filename)} bytes")
    print("\n" + "="*50)
    
    # Transcription phase
    print("🔤 TRANSCRIPTION PHASE")
    try:
        transcript = transcriber.transcribe_audio(audio_filename)
        if not transcript:
            print("❌ Transcription failed or returned empty result")
            return
        
        print(f"✅ Transcript length: {len(transcript)} characters")
        
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        return
    
    print("\n" + "="*50)
    
    # Summarization phase
    print("📝 SUMMARIZATION PHASE")
    try:
        summary = summarizer.summarize_transcript(transcript)
        action_items = summarizer.extract_action_items(transcript)
        
    except Exception as e:
        print(f"❌ Summarization error: {e}")
        summary = "Error generating summary"
        action_items = []
    
    print("\n" + "="*50)
    
    # Display results
    print("📋 MEETING RESULTS")
    print("="*50)
    
    print("\n📄 FULL TRANSCRIPT:")
    print("-" * 30)
    print(transcript)
    
    print(f"\n📝 SUMMARY:")
    print("-" * 30)
    print(summary)
    
    print(f"\n✅ ACTION ITEMS ({len(action_items)} found):")
    print("-" * 30)
    if action_items:
        for i, item in enumerate(action_items, 1):
            print(f"{i}. {item}")
    else:
        print("No action items detected.")
    
    print("\n" + "="*50)
    
    # Save results to file
    save_results_to_file(transcript, summary, action_items, timestamp)
    
    # Optional email sending
    send_email = input("\n📧 Send results via email? (y/n): ").lower().strip()
    if send_email == 'y':
        send_email_results(transcript, summary, action_items, timestamp)
    
    print("\n✅ Meeting processing completed!")
    print("🗂️  All files saved in current directory")

def save_results_to_file(transcript, summary, action_items, timestamp):
    """Save results to a text file"""
    filename = f"meeting_notes_{timestamp}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"MEETING NOTES - {timestamp}\n")
            f.write("="*50 + "\n\n")
            
            f.write("SUMMARY:\n")
            f.write("-"*20 + "\n")
            f.write(summary + "\n\n")
            
            f.write("ACTION ITEMS:\n")
            f.write("-"*20 + "\n")
            if action_items:
                for i, item in enumerate(action_items, 1):
                    f.write(f"{i}. {item}\n")
            else:
                f.write("No action items identified.\n")
            
            f.write("\nFULL TRANSCRIPT:\n")
            f.write("-"*20 + "\n")
            f.write(transcript + "\n")
        
        print(f"💾 Results saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")

def send_email_results(transcript, summary, action_items, timestamp):
    """Handle email sending with user input"""
    try:
        print("\n📧 EMAIL SETUP")
        print("Note: For Gmail, use an 'App Password' instead of your regular password")
        print("Generate one at: https://myaccount.google.com/apppasswords")
        
        email = input("Your email address: ").strip()
        password = input("Your app password (input hidden): ").strip()
        
        recipients_input = input("Recipients (comma-separated): ").strip()
        recipients = [r.strip() for r in recipients_input.split(',') if r.strip()]
        
        subject = f"Meeting Notes - {timestamp}"
        
        email_sender = EmailSender(email, password)
        success = email_sender.send_meeting_notes(
            recipients, subject, transcript, summary, action_items
        )
        
        if success:
            print("✅ Email sent successfully!")
        else:
            print("❌ Email sending failed")
            
    except Exception as e:
        print(f"❌ Email error: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Program interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
