print("Starting Flask server...")
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from calender_parser import parse_ical
from werkzeug.utils import secure_filename

load_dotenv()
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Connect to MongoDB
mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
db = client['ical_calendar']
events_collection = db['events']

# GET route to check server
@app.route('/')
def home():
    return "Flask server is running!"

# POST route to upload iCal file
@app.route('/upload', methods=['POST'])
def upload_ical():
    if 'ical' not in request.files:
        return "No file part", 400

    file = request.files['ical']
    if file.filename == '':
        return "No selected file", 400

    user_id = request.form.get('user_id', 'unknown')
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Parse iCal and store in MongoDB
    events = parse_ical(filepath)
    for event in events:
        event['user_id'] = user_id
    if events:
        events_collection.insert_many(events)

    return jsonify({"message": "iCal parsed and stored!", "events_count": len(events)})

# Optional: GET route to fetch all events for a user
@app.route('/events/<user_id>', methods=['GET'])
def get_events(user_id):
    events = list(events_collection.find({"user_id": user_id}, {"_id": 0}))
    return jsonify(events)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(port=int(os.getenv('PORT', 5000)), debug=True)
