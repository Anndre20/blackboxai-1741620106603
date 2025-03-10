import logging
from typing import Dict, Any, Optional, List
import openai
from .logger import setup_logger
from .integrations import MicrosoftIntegration, TimeTreeIntegration, GmailIntegration
from .file_manager import FileManager
from config import Config

logger = setup_logger()

class UnifiedAgent:
    def __init__(self):
        self.openai_api_key = Config.OPENAI_API_KEY
        openai.api_key = self.openai_api_key
        
        # Initialize all integrations
        self.ms_integration = MicrosoftIntegration()
        self.time_tree = TimeTreeIntegration()
        self.file_manager = FileManager()
        self.conversation_history: List[Dict[str, str]] = []

        # Command mappings for different functionalities
        self.commands = {
            'sort_files': self._handle_file_sorting,
            'sync_outlook': self._sync_outlook,
            'sync_onedrive': self._sync_onedrive,
            'sync_gmail': self._sync_gmail,
            'sync_calendar': self._sync_calendar,
            'sync_all': self._sync_all
        }

    def _get_ai_response(self, messages: List[Dict[str, str]]) -> str:
        """Get response from OpenAI API."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Failed to get AI response: {str(e)}")
            raise

    def _parse_intent(self, query: str) -> Dict[str, Any]:
        """Parse user query to determine intent and parameters."""
        try:
            # Add system message to help with intent parsing
            messages = [
                {
                    "role": "system",
                    "content": """You are an AI assistant that helps parse user intents. 
                    Identify the main action and extract relevant parameters. 
                    Respond in a structured format with 'intent' and 'params'.
                    Possible intents: sort_files, sync_outlook, sync_onedrive, sync_gmail, sync_calendar, sync_all, general_query"""
                },
                {"role": "user", "content": query}
            ]
            
            response = self._get_ai_response(messages)
            
            # Basic intent detection (can be enhanced with better NLP)
            intent = 'general_query'
            params = {}
            
            # File sorting intent
            if any(word in query.lower() for word in ['sort', 'organize', 'arrange']):
                intent = 'sort_files'
                # Extract potential parameters like source_dir, dest_dir, criteria
                if 'by type' in query.lower():
                    params['criteria'] = 'type'
                elif 'by date' in query.lower():
                    params['criteria'] = 'date'
                elif 'by size' in query.lower():
                    params['criteria'] = 'size'
                elif 'by name' in query.lower():
                    params['criteria'] = 'name'
            
            # Sync intents
            elif 'outlook' in query.lower():
                intent = 'sync_outlook'
            elif 'onedrive' in query.lower():
                intent = 'sync_onedrive'
            elif 'gmail' in query.lower():
                intent = 'sync_gmail'
            elif 'calendar' in query.lower() or 'timetree' in query.lower():
                intent = 'sync_calendar'
            elif 'sync' in query.lower() or 'synchronize' in query.lower():
                intent = 'sync_all'
            
            return {'intent': intent, 'params': params}
            
        except Exception as e:
            logger.error(f"Failed to parse intent: {str(e)}")
            return {'intent': 'general_query', 'params': {}}

    def _handle_file_sorting(self, params: Dict[str, Any]) -> str:
        """Handle file sorting requests."""
        try:
            if not params.get('source_dir') or not params.get('dest_dir'):
                return "Please provide both source and destination directories for file sorting."
            
            result = self.file_manager.sort_files(
                params['source_dir'],
                params['dest_dir'],
                params.get('criteria', 'type'),
                params.get('recursive', True)
            )
            
            if result['success']:
                stats = result['statistics']
                return f"Successfully sorted {stats['total_files']} files into categories. " \
                       f"Total size processed: {stats['total_size']} bytes."
            else:
                return f"Failed to sort files: {result['message']}"
                
        except Exception as e:
            logger.error(f"Error in file sorting: {str(e)}")
            return "An error occurred while sorting files."

    def _sync_outlook(self, params: Dict[str, Any]) -> str:
        """Sync Outlook emails and calendar."""
        try:
            data = self.ms_integration.get_outlook_data()
            return f"Successfully synced {len(data['emails'])} emails and {len(data['events'])} calendar events from Outlook."
        except Exception as e:
            logger.error(f"Error syncing Outlook: {str(e)}")
            return "Failed to sync Outlook data."

    def _sync_onedrive(self, params: Dict[str, Any]) -> str:
        """Sync OneDrive files."""
        try:
            files = self.ms_integration.get_onedrive_data()
            return f"Successfully synced {len(files)} files from OneDrive."
        except Exception as e:
            logger.error(f"Error syncing OneDrive: {str(e)}")
            return "Failed to sync OneDrive data."

    def _sync_gmail(self, params: Dict[str, Any]) -> str:
        """Sync Gmail."""
        try:
            # Note: Gmail integration requires proper authentication setup
            return "Gmail sync functionality will be available after authentication setup."
        except Exception as e:
            logger.error(f"Error syncing Gmail: {str(e)}")
            return "Failed to sync Gmail data."

    def _sync_calendar(self, params: Dict[str, Any]) -> str:
        """Sync calendar (TimeTree)."""
        try:
            events = self.time_tree.get_time_tree_data()
            return f"Successfully synced {len(events)} events from TimeTree calendar."
        except Exception as e:
            logger.error(f"Error syncing calendar: {str(e)}")
            return "Failed to sync calendar data."

    def _sync_all(self, params: Dict[str, Any]) -> str:
        """Sync all services."""
        try:
            results = []
            results.append(self._sync_outlook({}))
            results.append(self._sync_onedrive({}))
            results.append(self._sync_gmail({}))
            results.append(self._sync_calendar({}))
            return "\n".join(results)
        except Exception as e:
            logger.error(f"Error in sync_all: {str(e)}")
            return "Failed to sync all services."

    def process_query(self, query: str) -> str:
        """Main method to process user queries."""
        try:
            if not query:
                raise ValueError("Empty query received")
            
            logger.info(f"Processing query: {query}")
            
            # Add user query to conversation history
            self.conversation_history.append({"role": "user", "content": query})
            
            # Parse intent
            intent_data = self._parse_intent(query)
            intent = intent_data['intent']
            params = intent_data['params']
            
            # Execute corresponding command if available
            if intent in self.commands:
                response = self.commands[intent](params)
            else:
                # Handle general queries with AI
                messages = [
                    {
                        "role": "system",
                        "content": """You are a helpful AI assistant with the following capabilities:
                        - File sorting and organization
                        - Microsoft Outlook integration
                        - Microsoft OneDrive integration
                        - Gmail integration
                        - TimeTree calendar integration
                        You can help users manage their emails, files, and calendar events."""
                    },
                    *self.conversation_history
                ]
                response = self._get_ai_response(messages)
            
            # Add response to conversation history
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # Keep conversation history manageable
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return response
            
        except ValueError as ve:
            logger.warning(f"Invalid query: {str(ve)}")
            return "Please provide a valid query."
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return "I encountered an error while processing your request. Please try again later."

    def reset_conversation(self) -> None:
        """Reset the conversation history."""
        self.conversation_history = []
