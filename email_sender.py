import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailSender:
    def __init__(self, email, password):
        """Initialize email sender with credentials"""
        self.email = email
        self.password = password
    
    def send_meeting_notes(self, recipients, subject, transcript, summary, action_items):
        """Send meeting notes via email"""
        print("📧 Preparing to send meeting notes...")
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            
            # Create email body
            body = self.format_email_body(transcript, summary, action_items)
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email using Gmail SMTP
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()  # Enable encryption
            server.login(self.email, self.password)
            
            text = msg.as_string()
            server.sendmail(self.email, recipients, text)
            server.quit()
            
            print("✅ Meeting notes sent successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False
    
    def format_email_body(self, transcript, summary, action_items):
        """Format the email body with meeting notes"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        body = f"""
MEETING NOTES - {timestamp}
{'='*50}

EXECUTIVE SUMMARY:
{'-'*20}
{summary}

ACTION ITEMS:
{'-'*20}
"""
        
        if action_items:
            for i, item in enumerate(action_items, 1):
                body += f"{i}. {item}\n"
        else:
            body += "No specific action items identified.\n"
        
        body += f"""

FULL TRANSCRIPT:
{'-'*20}
{transcript}

---
Generated automatically by Meeting Assistant
"""
        
        return body
