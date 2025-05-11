from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tasks = [
    {
        "id": id,
        "title": "Task",
        "description": "Description",
        "completed": False,
    }
    for id in range(10)
]


@app.route("/tasks")
def list_tasks():
    return tasks


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def edit_task(task_id: int):
    data = request.json
    task = {
        "id": task_id,
        "title": data["title"],
        "description": data["description"],
        "completed": data["completed"],
    }
    tasks[task_id] = task
    return task
