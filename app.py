from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

TASKS = [
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
    return TASKS


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def edit_task(task_id: int):
    data = request.json
    task = {
        "id": task_id,
        "title": data["title"],
        "description": data["description"],
        "completed": data["completed"],
    }
    task_index = [index for (index, task) in enumerate(TASKS) if task["id"] == task_id][
        0
    ]
    TASKS[task_index] = task
    return task


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id: int):
    task_index = [index for (index, task) in enumerate(TASKS) if task["id"] == task_id][
        0
    ]
    del TASKS[task_index]
    return "", 204
