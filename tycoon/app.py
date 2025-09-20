from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from User import User
from Task import Task

app = Flask(__name__)
CORS(app)

# Simple in-memory store (replace with MongoDB later)
users = {}

def get_user(username: str) -> User:
    if username not in users:
        users[username] = User(username)
    return users[username]

# ---------------- TASK ROUTES ---------------- #

@app.post("/tasks")
def create_task():
    data = request.json
    username = data.get("username")
    title = data.get("title")
    duration_min = data.get("durationMin", 30)

    if not username or not title:
        return jsonify({"error": "username and title are required"}), 400

    user = get_user(username)
    task = Task(title=title, duration=duration_min)
    user.add_task(task)

    return jsonify({"id": task.id, "title": task.title, "duration": task.duration})

@app.post("/tasks/<username>/<task_id>/complete")
def complete_task(username, task_id):
    user = get_user(username)

    task = next((t for t in user.to_do_tasks if str(t.id) == str(task_id)), None)
    if not task:
        return jsonify({"error": f"Task {task_id} not found"}), 404

    task_time = datetime.now()
    user.finish_task(task)
    user.last_completed_task_time = task_time

    return jsonify({
        "xp": user.xp,
        "level": user.level,
        "streak": user.streak
    })

@app.get("/tasks/autofit")
def autofit():
    username = request.args.get("userId")
    if not username:
        return jsonify({"error": "userId required"}), 400

    # Placeholder scheduling logic
    user = get_user(username)
    scheduled = len(user.to_do_tasks)

    return jsonify({"scheduled": scheduled})

# ---------------- USER ROUTES ---------------- #

@app.get("/users/<username>/xp")
def get_xp(username):
    user = get_user(username)
    return jsonify({
        "xp": user.xp,
        "level": user.level,
        "streak": user.streak
    })

@app.get("/users/<username>/summary")
def get_summary(username):
    user = get_user(username)
    return jsonify(user.summary())

@app.post("/users/<username>/purchase-upgrade")
def purchase_upgrade(username):
    user = get_user(username)
    data = request.json
    upgrade_name = data.get("upgrade")
    success = user.purchase_upgrade(upgrade_name)
    return jsonify({"success": success, "xp": user.xp, "upgrades": user.upgrades})

@app.post("/users/<username>/rebirth")
def rebirth(username):
    user = get_user(username)
    user.rebirth()
    return jsonify({"rebirths": user.rebirths, "permanent_boost": user.permanent_boost})

@app.get("/users/<username>/passive-xp")
def passive_xp(username):
    user = get_user(username)
    user.constant_income()
    return jsonify({
        "xp": user.xp,
        "level": user.level,
        "streak": user.streak
    })

# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    app.run(port=8000, debug=True)
