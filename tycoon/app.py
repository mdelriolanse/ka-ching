import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from User import User
from Task import Task
from icalendar import Calendar
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from pymongo import MongoClient

# Connect to Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['UPLOAD_FOLDER'] = 'uploads/'
load_dotenv()

# Connect to MongoDB
mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
db = client['ical_calendar']
events_collection = db['events']

# In-memory stores
users = {}
tasks = {}

# Helper
def get_or_create_user(username: str) -> User:
    if username not in users:
        users[username] = User(username)
    return users[username]

# -------------------------
# User endpoints
# -------------------------
@app.route("/users/<username>/xp", methods=["GET"])
def get_user_xp(username):
    try:
        user = get_or_create_user(username)
        return jsonify(user.summary())
    except Exception as e:
        print(f"Error fetching user XP: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/users/<username>/upgrades/<upgrade_name>", methods=["POST"])
def purchase_upgrade(username, upgrade_name):
    try:
        user = get_or_create_user(username)
        success = user.purchase_upgrade(upgrade_name)
        return jsonify({"success": success, "summary": user.summary()})
    except Exception as e:
        print(f"Error purchasing upgrade: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/users/<username>/rebirth", methods=["POST"])
def rebirth(username):
    try:
        user = get_or_create_user(username)
        success = user.rebirth()
        return jsonify({"success": success, "summary": user.summary()})
    except Exception as e:
        print(f"Error during rebirth: {e}")
        return jsonify({"error": str(e)}), 500

# -------------------------
# Task endpoints
# -------------------------
@app.route("/tasks", methods=["POST"])
def create_task():
    try:
        data = request.json
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON payload"}), 400

        username = data.get("username")
        title = data.get("title")
        duration = data.get("durationMin", 25)

        if not username or not isinstance(username, str):
            return jsonify({"error": "Missing or invalid username"}), 400
        if not title or not isinstance(title, str):
            return jsonify({"error": "Missing or invalid title"}), 400

        try:
            duration_val = int(duration)
        except Exception:
            print(f"Error converting durationMin: {duration}")
            return jsonify({"error": "durationMin must be an integer"}), 400

        task = Task(title, durationMin=duration_val, xp_reward=duration_val)
        tasks[task.id] = task

        user = get_or_create_user(username)
        user.add_task(task)

        return jsonify({
            "id": task.id,
            "title": task.title,
            "durationMin": duration,
            "xp_reward": task.xp_reward
        })
    except Exception as e:
        print(f"Error creating task: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/tasks/<task_id>/complete", methods=["POST"])
def complete_task(task_id):
    try:
        data = request.json
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON payload"}), 400

        username = data.get("username")
        if not username or not isinstance(username, str):
            return jsonify({"error": "Missing or invalid username"}), 400

        user = get_or_create_user(username)

        task = tasks.get(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        # Ensure the user actually has the task
        if task not in user.to_do_tasks:
            return jsonify({"error": "Task not assigned to user"}), 403

        user.finish_task(task)
        return jsonify({
            "xp": user.xp,
            "level": user.level,
            "streak": user.streak
        })
    except Exception as e:
        print(f"Error completing task: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/tasks/autofit", methods=["POST"])
def autofit():
    try:
        data = request.json
        username = data.get("username")
        user = get_or_create_user(username)
        # TODO: implement scheduling logic
        return jsonify({"message": f"Autofit not yet implemented for {username}"})
    except Exception as e:
        print(f"Error in autofit: {e}")
        return jsonify({"error": str(e)}), 500
    
# -------------------------
# MongoDB + iCal endpoints
# -------------------------

def parse_ical(file_path):
    try:
        with open(file_path, 'rb') as f:
            gcal = Calendar.from_ical(f.read())

        events = []
        for component in gcal.walk():
            if component.name == "VEVENT":
                event = {
                    "title": str(component.get('summary')),
                    "description": str(component.get('description') or ""),
                    "location": str(component.get('location') or ""),
                    "start": component.get('dtstart').dt.isoformat(),
                    "end": component.get('dtend').dt.isoformat()
                }
                events.append(event)
        return events
    except Exception as e:
        print(f"Error parsing iCal file: {e}")
        return []

# POST route to upload iCal file
@app.route('/upload', methods=['POST'])
def upload_ical():
    try:
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
    except Exception as e:
        print(f"Error uploading iCal: {e}")
        return jsonify({"error": str(e)}), 500

# Optional: GET route to fetch all events for a user
@app.route('/events/<user_id>', methods=['GET'])
def get_events(user_id):
    try:
        events = list(events_collection.find({"user_id": user_id}, {"_id": 0}))
        return jsonify(events)
    except Exception as e:
        print(f"Error fetching events: {e}")
        return jsonify({"error": str(e)}), 500
    
# -------------------------
# Run server
# -------------------------
if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    # bind to 0.0.0.0 so frontend running on localhost can reach this container/host
    app.run(debug=True, host="0.0.0.0", port=8000)
