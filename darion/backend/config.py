import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Basic Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # Microsoft Graph API Configuration (for Outlook, OneDrive, and other Microsoft apps)
    MS_GRAPH_CLIENT_ID = os.environ.get('MS_GRAPH_CLIENT_ID')
    MS_GRAPH_CLIENT_SECRET = os.environ.get('MS_GRAPH_CLIENT_SECRET')
    MS_GRAPH_TENANT_ID = os.environ.get('MS_GRAPH_TENANT_ID')
    MS_GRAPH_SCOPES = [
        'User.Read',
        'Mail.Read',
        'Mail.Send',
        'Calendars.ReadWrite',
        'Files.ReadWrite',
    ]
    
    # Gmail API Configuration
    GMAIL_CLIENT_ID = os.environ.get('GMAIL_CLIENT_ID')
    GMAIL_CLIENT_SECRET = os.environ.get('GMAIL_CLIENT_SECRET')
    GMAIL_SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.send',
    ]
    
    # TimeTree API Configuration
    TIMETREE_ACCESS_TOKEN = os.environ.get('TIMETREE_ACCESS_TOKEN')
    TIMETREE_CALENDAR_ID = os.environ.get('TIMETREE_CALENDAR_ID')
    
    # Redis Configuration (for caching)
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # API Endpoints
    MS_GRAPH_ENDPOINT = 'https://graph.microsoft.com/v1.0'
    GMAIL_API_ENDPOINT = 'https://www.googleapis.com/gmail/v1/users/me'
    TIMETREE_API_ENDPOINT = 'https://timetreeapis.com'
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    
    # Cache Configuration
    CACHE_TIMEOUT = int(os.environ.get('CACHE_TIMEOUT') or 300)  # 5 minutes default
    
    @staticmethod
    def init_app(app):
        """Initialize application with this configuration"""
        pass
