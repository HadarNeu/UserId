from flask import Flask, jsonify, render_template_string
import requests
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hi! This is my user ID app home page'

@app.route('/json')
def get_json():
    response = requests.get('https://jsonplaceholder.typicode.com/todos')
    return jsonify(response.json())


@app.route('/json/user/<int:user_id>', methods=['GET'])
def present_users_matadata(user_id):
    users_data = get_json()
    users_metadata = extract_user_metadata(users_data, user_id)

    if not users_metadata:
        return f"The user you have requested does not exist in our DB. Please try again! "
    return format_metadata(users_metadata)

# Custom handler for 404 errors
@app.errorhandler(404)
def page_not_found(error):
    return f"The page you are looking for does not exist. Please look for an integer!", 404


def extract_user_metadata(all_data, user_id):
    """
    Extract raw metadata for a specific user.
    
    Args:
        users_data (list): List of todo dictionaries
        user_id (int): User ID to extract metadata for
    
    Returns:
        dict: Raw metadata for the specified user
    """

    all_metadata = all_data.get_json()
    # Filter users_metadata for the specific user
    user_metadata = [todo for todo in all_metadata if todo['userId'] == user_id]

    print(f"this is the users_mtadata from the extract method {user_metadata}")
    return user_metadata

def format_metadata(metadata):
    """
    Format metadata into readable blocks.
    
    Args:
        metadata (dict): Metadata dictionary
    
    Returns:
        str: Formatted metadata
    """
    formatted = f"User ID: {metadata[0]['userId']}\n"
    formatted += "="*40 + "\n"
    
    for todo in metadata:
        #completed readable: completed vs incomplete
        completed_status = "Completed" if todo['completed'] else "Incomplete" 
        formatted += f"Todo ID: {todo['id']}\n"
        formatted += f"Title: {todo['title']}\n"
        formatted += f"Completed: {completed_status}\n"
        formatted += "-"*40 + "\n\n"

    
    formatted_html = formatted.replace('\n', '<br>') 

    formatted_html_rendered = render_template_string(formatted_html)    
    
    return f"<pre>{formatted_html_rendered}</pre>"


if __name__ == '__main__':
    app.run(debug=True)