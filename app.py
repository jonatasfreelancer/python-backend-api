# Import necessary modules from Flask
from flask import Flask, jsonify, request, abort

# Initialize the Flask application
app = Flask(__name__)

# --- In-memory data store for tasks (Our temporary 'database') ---
# This is a simple list of dictionaries that acts as our "database".
tasks = [
    {
        'id': 1,
        'title': 'Buy groceries',
        'description': 'Milk, Cheese, Pizza, Fruit'
    },
    {
        'id': 2,
        'title': 'Learn Python',
        'description': 'Find a good Python tutorial on the web'
    }
]

# --- Error Handling (Professional Touch) ---
# Define a custom 404 handler for resources not found (e.g., /users instead of /tasks)
@app.errorhandler(404)
def not_found(error):
    # Returns a 404 status code with a clean JSON error payload
    return jsonify({'error': 'Not Found'}), 404

# Define a custom 415 handler for unsupported media type (The Content-Type error)
@app.errorhandler(415)
def unsupported_media_type(error):
    # Returns a 415 status code with a message explaining the JSON requirement
    return jsonify({'error': 'Unsupported Media Type: Request must be JSON (Content-Type: application/json)'}), 415

# --- Define API Endpoints ---
# Handles requests for the tasks collection.
# We use /tasks to follow standard REST API conventions.
@app.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    """
    Handles requests for the tasks collection.
    GET: Returns the list of all tasks.
    POST: Creates a new task.
    """
    if request.method == 'GET':
        # GET: Returns the list of all tasks
        return jsonify({'tasks': tasks})

    elif request.method == 'POST':
        # POST: Creates a new task

        # 1. Check if the request body is valid JSON
        # This handles the 415 error if Content-Type is missing or wrong
        if not request.is_json:
            abort(415) 
        
        # 2. Validate essential fields (title and description)
        if 'title' not in request.json or 'description' not in request.json:
            # Returns a 400 Bad Request if mandatory fields are missing
            return jsonify({'error': "Missing mandatory field: 'title' and 'description' are required"}), 400

        # 3. Create the new task dictionary
        new_task = {
            # Generates a new ID based on the last task's ID, or starts at 1
            'id': tasks[-1]['id'] + 1 if tasks else 1, 
            'title': request.json['title'],
            'description': request.json['description'],
        }
        
        # 4. Add the new task to the in-memory list
        tasks.append(new_task)

        # 5. Return the newly created task with a 201 Created status code
        return jsonify({'task': new_task}), 201

# --- Main execution block to run the Flask app ---
if __name__ == '__main__':
    # Running on 0.0.0.0 makes it accessible to the network, which is a good practice.
    app.run(debug=True, host='0.0.0.0')