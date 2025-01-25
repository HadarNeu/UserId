from flask import Flask, jsonify, render_template_string
import requests
import typing
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)] # Log to console
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    """
    Render the home page of the application.
    
    Returns:
        str: Welcome message
    """
    logger.info('Home page accessed')
    return 'Hi! This is my user ID app home page'

@app.route('/json')
def get_json():
    """
    Fetch entries from JSONPlaceholder API.
    
    Returns:
        flask.Response: JSON response of todo entries
    """
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/todos')
        logger.info(f'Successfully fetched {len(response.json())}')
        return jsonify(response.json())
    except requests.RequestException as e:
        logger.error(f'Error fetching todos: {e}')
        return jsonify({'error': 'Failed to fetch todos'}), 500

@app.route('/json/user/<int:user_id>', methods=['GET'])
def present_users_data(user_id: int):
    """
    Retrieve and present data for a specific user.
    
    Args:
        user_id (int): Unique identifier for the user
    
    Returns:
        str: Formatted user data or 404 error message
    """
    logger.info(f'Requested data for user ID: {user_id}')
    
    try:
        all_data = get_json()
        user_entries = extract_user_entries(all_data, user_id)

        if not user_entries:
            logger.warning(f'User ID {user_id} not found')
            return "The user you have requested does not exist in our DB. Please try again!", 404
        
        return format_data(user_entries)
    except Exception as e:
        logger.error(f'Unexpected error processing user {user_id}: {e}')
        return "An unexpected error occurred", 500

@app.errorhandler(404)
def page_not_found(error):
    """
    Custom 404 error handler.
    
    Args:
        error: Flask error object
    
    Returns:
        str: Error message with 404 status code
    """
    logger.warning(f'404 error occurred: {error}')
    return "The page you are looking for does not exist. Remember, user ID's are integers only!", 404

def extract_user_entries(all_data, user_id: int) -> typing.List[dict]:
    """
    Extract entries for a specific user.
    
    Args:
        all_data (flask.Response): Full list of entries
        user_id (int): User identifier to filter entries
    
    Returns:
        List of entries for the specified user
    """
    entries = all_data.get_json()
    filtered_entries = [entry for entry in entries if entry['userId'] == user_id]
    logger.info(f'Extracted {len(filtered_entries)} entries for user ID {user_id}')
    return filtered_entries

def format_data(user_entries: typing.List[dict]) -> str:
    """
    Convert user entries into a human-readable HTML format.
    
    Args:
        user_entries (List[dict]): Entries for a specific user
    
    Returns:
        Formatted HTML representation of user entries
    """
    if not user_entries:
        logger.warning('No data available for formatting')
        return "No data available for this user ID. Please try another one!"

    formatted = f"User ID: {user_entries[0]['userId']}\n"
    formatted += "="*40 + "\n"
    
    for entry in user_entries:
        status = "Completed" if entry.get('completed', 'undefined') else "Incomplete" 
        formatted += (
            f"Entry ID: {entry.get('id', 'undefined')}\n"
            f"Title: {entry.get('title', 'undefined')}\n"
            f"Status: {status}\n"
            f"{'-'*40}\n\n"
        )

    formatted_html = formatted.replace('\n', '<br>') 
    logger.info(f'Presenting formatted data for user ID {user_entries[0]["userId"]}')
    return f"<pre>{render_template_string(formatted_html)}</pre>"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)