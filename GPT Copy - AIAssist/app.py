
from flask import Flask, request, jsonify,g
from ml_model import super_chat_gpt_like_model
from sqlalchemy.orm import sessionmaker
from db_model import DBModel, engine
from authentication import auth
import uuid

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

# Dictionary to store job statuses
job_statuses = {}

# Limit of calls per user
CALL_LIMIT_PER_USER = 3

# Dictionary to track the number of calls per user
user_call_counts = {}

# Health check endpoint
@app.route('/health_check')
def health_check():
    return '', 204

# Endpoint to call the ML model with authentication and database storage
@app.route('/call_model', methods=['POST'])
@auth.login_required
def call_model():
    prompt = request.json['prompt'] 
    response = super_chat_gpt_like_model(prompt)
    
    # Storing response in the database
    # Replace with actual database session management
    db_entry = DBModel(user_id=auth.current_user(), prompt=prompt, response=response)
    session.add(db_entry)
    session.commit()

    return jsonify(response=response), 201

# Endpoint for asynchronous ML model call
@app.route('/async_call_model', methods=['POST'])
@auth.login_required
def async_call_model():
    # Check if the user has already reached the call limit
    user_id = auth.current_user()
    if user_id not in user_call_counts:    
        user_call_counts[user_id] = 0
    if user_call_counts[user_id] >= CALL_LIMIT_PER_USER:
        return 'You have reached the maximum call limit', 403  # Forbidden
    
    # Extract the 'prompt' data from the JSON request payload
    prompt = request.json['prompt']
    # Generate a unique job ID using UUID version 4
    job_id = str(uuid.uuid4())
    
    # Update the call count for the user
    user_call_counts[user_id] += 1
    
    # Start a new asynchronous task to process the prompt
    # You can use libraries like Celery for task queuing
    job_statuses[job_id] = {'status': 'processing', 'response': None}
    return jsonify(job_id=job_id), 200

# Endpoint to check status of asynchronous job
@app.route('/async_call_status', methods=['GET'])
@auth.login_required
def async_call_status():
    job_id = request.args.get('job_id')
    if job_id in job_statuses:
        return jsonify(job_status=job_statuses[job_id]['status'], response=job_statuses[job_id]['response']), 200
    else:
        return 'Job ID not found', 404

if __name__ == '__main__':
    app.run(debug=True)
