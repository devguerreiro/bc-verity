from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/tasks")
def list_tasks():
    task = {
        "title": "Task",
        "description": "Description",
        "completed": False,
    }
    return [{**task, "id": x} for x in range(10)]
