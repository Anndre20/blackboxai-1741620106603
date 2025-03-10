from flask import Flask, request, jsonify
from flask_cors import CORS
from modules.ai_agent import UnifiedAgent
from modules.logger import setup_logger
from config import Config

app = Flask(__name__)
CORS(app)
logger = setup_logger()

# Initialize unified agent
agent = UnifiedAgent()

@app.route('/api/ai-query', methods=['POST'])
def ai_query():
    """Handle AI queries and return responses."""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'No query provided'}), 400
        
        query = data['query']
        response = agent.process_query(query)
        return jsonify({'response': response})
    
    except Exception as e:
        logger.error(f"Error processing AI query: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/sync/outlook', methods=['GET'])
def sync_outlook():
    """Synchronize Outlook data."""
    try:
        response = agent.process_query("sync outlook")
        return jsonify({'response': response})
    except Exception as e:
        logger.error(f"Error syncing Outlook: {str(e)}")
        return jsonify({'error': 'Failed to sync Outlook data'}), 500

@app.route('/api/sync/onedrive', methods=['GET'])
def sync_onedrive():
    """Synchronize OneDrive data."""
    try:
        response = agent.process_query("sync onedrive")
        return jsonify({'response': response})
    except Exception as e:
        logger.error(f"Error syncing OneDrive: {str(e)}")
        return jsonify({'error': 'Failed to sync OneDrive data'}), 500

@app.route('/api/sync/timetree', methods=['GET'])
def sync_timetree():
    """Synchronize TimeTree data."""
    try:
        response = agent.process_query("sync calendar")
        return jsonify({'response': response})
    except Exception as e:
        logger.error(f"Error syncing TimeTree: {str(e)}")
        return jsonify({'error': 'Failed to sync TimeTree data'}), 500

@app.route('/api/sync/all', methods=['GET'])
def sync_all():
    """Synchronize data from all services."""
    try:
        response = agent.process_query("sync all")
        return jsonify({'response': response})
    except Exception as e:
        logger.error(f"Error syncing all services: {str(e)}")
        return jsonify({'error': 'Failed to sync all services'}), 500

@app.route('/api/conversation/reset', methods=['POST'])
def reset_conversation():
    """Reset the AI agent's conversation history."""
    try:
        agent.reset_conversation()
        return jsonify({'message': 'Conversation history reset successfully'})
    except Exception as e:
        logger.error(f"Error resetting conversation: {str(e)}")
        return jsonify({'error': 'Failed to reset conversation'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})

@app.route('/')
def home():
    """Home endpoint."""
    return "Welcome to Darion - Your AI-Powered Digital Assistant!"

if __name__ == '__main__':
    app.config.from_object(Config)
    app.run(debug=True)
