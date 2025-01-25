from flask import Flask, jsonify, render_template_string
import requests
import typing

app = Flask(__name__)

@app.route('/')
def home():
    """
    Render the home page of the application.
    
    Returns:
        str: Welcome message
    """
    return 'Hi! This is my user ID app home page'

@app.route('/json')
def get_json():
    """
    Fetch todos from JSONPlaceholder API.
    
    Returns:
        flask.Response: JSON response of todos
    """
    response = requests.get('https://jsonplaceholder.typicode.com/todos')
    return jsonify(response.json())

@app.route('/json/user/<int:user_id>', methods=['GET'])
def present_users_data(user_id: int):
    """
    Retrieve and present data for a specific user.
    
    Args:
        user_id (int): Unique identifier for the user
    
    Returns:
        str: Formatted user data or 404 error message
    """
    all_data = get_json()
    user_entries = extract_user_entries(all_data, user_id)

    if not user_entries:
        return "The user you have requested does not exist in our DB. Please try again!", 404
    
    return format_data(user_entries)

@app.errorhandler(404)
def page_not_found(error):
    """
    Custom 404 error handler.
    
    Args:
        error: Flask error object
    
    Returns:
        str: Error message with 404 status code
    """
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
    return [entry for entry in entries if entry['userId'] == user_id]

def format_data(user_entries: typing.List[dict]) -> str:
    """
    Convert user entries into a human-readable HTML format.
    
    Args:
        user_entries (List[dict]): Entries for a specific user
    
    Returns:
        Formatted HTML representation of user entries
    """
    if not user_entries:
        return "No data available"

    formatted = f"User ID: {user_entries[0]['userId']}\n"
    formatted += "="*40 + "\n"
    
    for entry in user_entries:
        status = "Completed" if entry.get('completed', 'N/A') else "Incomplete" 
        formatted += (
            f"Entry ID: {entry.get('id', 'N/A')}\n"
            f"Title: {entry.get('title', 'No title')}\n"
            f"Status: {status}\n"
            f"{'-'*40}\n\n"
        )

    formatted_html = formatted.replace('\n', '<br>') 
    return f"<pre>{render_template_string(formatted_html)}</pre>"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)