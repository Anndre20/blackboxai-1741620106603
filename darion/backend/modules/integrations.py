import logging
from typing import Dict, Any, List
import requests
from msal import ConfidentialClientApplication
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from config import Config
from .logger import setup_logger

logger = setup_logger()

class MicrosoftIntegration:
    def __init__(self):
        self.client_id = Config.MS_GRAPH_CLIENT_ID
        self.client_secret = Config.MS_GRAPH_CLIENT_SECRET
        self.tenant_id = Config.MS_GRAPH_TENANT_ID
        self.scopes = Config.MS_GRAPH_SCOPES
        self.endpoint = Config.MS_GRAPH_ENDPOINT
        self.app = ConfidentialClientApplication(
            self.client_id,
            authority=f"https://login.microsoftonline.com/{self.tenant_id}",
            client_credential=self.client_secret,
        )

    def get_access_token(self) -> str:
        """Get Microsoft Graph API access token."""
        try:
            result = self.app.acquire_token_silent(self.scopes, account=None)
            if not result:
                result = self.app.acquire_token_for_client(scopes=self.scopes)
            return result['access_token']
        except Exception as e:
            logger.error(f"Failed to get Microsoft access token: {str(e)}")
            raise

    def get_outlook_data(self) -> Dict[str, Any]:
        """Fetch emails and calendar events from Outlook."""
        try:
            token = self.get_access_token()
            headers = {'Authorization': f'Bearer {token}'}
            
            # Get emails
            emails_response = requests.get(
                f"{self.endpoint}/me/messages",
                headers=headers
            )
            emails_response.raise_for_status()
            
            # Get calendar events
            events_response = requests.get(
                f"{self.endpoint}/me/events",
                headers=headers
            )
            events_response.raise_for_status()
            
            return {
                'emails': emails_response.json().get('value', []),
                'events': events_response.json().get('value', [])
            }
        except Exception as e:
            logger.error(f"Failed to fetch Outlook data: {str(e)}")
            raise

    def get_onedrive_data(self) -> List[Dict[str, Any]]:
        """Fetch files and folders from OneDrive."""
        try:
            token = self.get_access_token()
            headers = {'Authorization': f'Bearer {token}'}
            
            response = requests.get(
                f"{self.endpoint}/me/drive/root/children",
                headers=headers
            )
            response.raise_for_status()
            
            return response.json().get('value', [])
        except Exception as e:
            logger.error(f"Failed to fetch OneDrive data: {str(e)}")
            raise

class GmailIntegration:
    def __init__(self, credentials: Credentials):
        self.service = build('gmail', 'v1', credentials=credentials)

    def get_gmail_data(self) -> Dict[str, Any]:
        """Fetch emails from Gmail."""
        try:
            results = self.service.users().messages().list(userId='me').execute()
            messages = results.get('messages', [])
            
            emails = []
            for message in messages[:10]:  # Limit to 10 most recent emails
                msg = self.service.users().messages().get(
                    userId='me', 
                    id=message['id']
                ).execute()
                emails.append(msg)
            
            return {'emails': emails}
        except Exception as e:
            logger.error(f"Failed to fetch Gmail data: {str(e)}")
            raise

class TimeTreeIntegration:
    def __init__(self):
        self.access_token = Config.TIMETREE_ACCESS_TOKEN
        self.calendar_id = Config.TIMETREE_CALENDAR_ID
        self.endpoint = Config.TIMETREE_API_ENDPOINT
        
    def get_time_tree_data(self) -> Dict[str, Any]:
        """Fetch calendar events from TimeTree."""
        try:
            headers = {
                'Accept': 'application/vnd.timetree.v1+json',
                'Authorization': f'Bearer {self.access_token}'
            }
            
            response = requests.get(
                f"{self.endpoint}/calendars/{self.calendar_id}/upcoming_events",
                headers=headers
            )
            response.raise_for_status()
            
            return response.json().get('data', [])
        except Exception as e:
            logger.error(f"Failed to fetch TimeTree data: {str(e)}")
            raise

def sync_all_data() -> Dict[str, Any]:
    """Synchronize data from all integrated services."""
    try:
        ms_integration = MicrosoftIntegration()
        time_tree = TimeTreeIntegration()
        
        # Note: Gmail integration requires credentials to be passed
        # gmail_integration = GmailIntegration(credentials)
        
        return {
            'outlook': ms_integration.get_outlook_data(),
            'onedrive': ms_integration.get_onedrive_data(),
            'timetree': time_tree.get_time_tree_data(),
            # 'gmail': gmail_integration.get_gmail_data()
        }
    except Exception as e:
        logger.error(f"Failed to sync all data: {str(e)}")
        raise
