from transformers import pipeline
import re

class MeetingSummarizer:
    def __init__(self):
        """Initialize summarization model"""
        print("📥 Loading summarization model...")
        try:
            self.summarizer = pipeline(
                "summarization", 
                model="sshleifer/distilbart-cnn-12-6",
                device=-1  # Use CPU
            )
            print("✅ Summarization model loaded!")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.summarizer = None
    
    def summarize_transcript(self, transcript, max_length=150):
        """Create summary from transcript"""
        if not self.summarizer:
            return "Summarization unavailable - model failed to load"
        
        if len(transcript) < 100:
            return "Transcript too short to summarize effectively"
        
        print("🔄 Generating summary...")
        
        # Split long text into chunks
        chunk_size = 1000
        chunks = [transcript[i:i+chunk_size] 
                 for i in range(0, len(transcript), chunk_size)]
        
        summaries = []
        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) > 50:
                try:
                    summary = self.summarizer(
                        chunk, 
                        max_length=max_length, 
                        min_length=30, 
                        do_sample=False
                    )
                    summaries.append(summary[0]['summary_text'])
                    print(f"✅ Summarized chunk {i+1}/{len(chunks)}")
                except Exception as e:
                    print(f"⚠️ Error summarizing chunk {i+1}: {e}")
        
        final_summary = ' '.join(summaries)
        print("✅ Summary generation completed!")
        return final_summary
    
    def extract_action_items(self, transcript):
        """Extract action items from transcript"""
        print("🔄 Extracting action items...")
        
        # Keywords that indicate action items
        action_keywords = [
            'action item', 'action point', 'todo', 'to do', 'task', 
            'follow up', 'follow-up', 'next step', 'assign', 'assigned',
            'deadline', 'due date', 'homework', 'deliverable',
            'responsible for', 'will do', 'needs to', 'must do'
        ]
        
        sentences = re.split(r'[.!?]+', transcript)
        action_items = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:  # Skip very short sentences
                for keyword in action_keywords:
                    if keyword.lower() in sentence.lower():
                        action_items.append(sentence)
                        break
        
        # Remove duplicates while preserving order
        unique_actions = []
        for item in action_items:
            if item not in unique_actions:
                unique_actions.append(item)
        
        print(f"✅ Found {len(unique_actions)} action items")
        return unique_actions[:10]  # Limit to top 10 items
