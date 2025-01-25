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
def present_users_data(user_id):
    all_data = get_json()
    users_data = extract_user_data(all_data, user_id)

    if not users_data:
        return f"The user you have requested does not exist in our DB. Please try again! ", 404
    return format_data(users_data)

# Custom handler for 404 errors
@app.errorhandler(404)
def page_not_found(error):
    return f"The page you are looking for does not exist. Remember, user ID's are integers only!", 404


def extract_user_data(all_data, user_id):
    """
    Extract raw data for a specific user.
    
    Args:
        all_data (list): List of users data dictionaries
        user_id (int): User ID to extract data for
    
    Returns:
        dict: Raw data for the specified user
    """

    all_data = all_data.get_json()
    # Filters data for the specific user
    user_data = [key for key in all_data if key['userId'] == user_id]
    return user_data

def format_data(users_data):
    """
    Format users data into readable blocks.
    
    Args:
        users_data(list): specific users data list that contains dictionaries as objects. 
    
    Returns:
        str: Formatted data
    """
    formatted = f"User ID: {users_data[0]['userId']}\n"
    formatted += "="*40 + "\n"
    
    for key in users_data:
        # convert Completed bool value to a more readable value: completed vs incomplete
        completed_status = "Completed" if key['completed'] else "Incomplete" 
        formatted += f"Todo ID: {key['id']}\n"
        formatted += f"Title: {key['title']}\n"
        formatted += f"Completed: {completed_status}\n"
        formatted += "-"*40 + "\n\n"

    # replacing newline with <br> to get the newline effect in Flask. 
    formatted_html = formatted.replace('\n', '<br>') 
    formatted_html_rendered = render_template_string(formatted_html)    
    return f"<pre>{formatted_html_rendered}</pre>"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)