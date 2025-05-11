from sqlite3 import IntegrityError
from flask import request, Blueprint

from app.db import get_db
from app.task.repository import TaskRepository


bp = Blueprint("task", __name__, url_prefix="/task")


@bp.get("/")
def list_tasks():
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))
    offset = (page - 1) * page_size
    db = get_db()
    repo = TaskRepository(db)
    tasks = repo.findAll(page_size, offset)
    total_count = db.execute("SELECT COUNT(*) FROM task").fetchone()[0]
    db.close()
    return {
        "page": page,
        "page_size": page_size,
        "total": total_count,
        "results": tasks,
    }


@bp.post("/")
def create_task():
    try:
        data = request.json
        task = {
            "title": data["title"],
            "description": data.get("description"),
        }
        db = get_db()
        repo = TaskRepository(db)
        created_task = repo.create(task["title"], task["description"])
        db.close()
        return created_task
    except KeyError as err:
        return f"{err} is required", 400


@bp.put("/<int:task_id>")
def edit_task(task_id: int):
    data = request.json
    task = {
        "title": data["title"],
        "description": data["description"],
        "completed": data["completed"],
    }
    db = get_db()
    repo = TaskRepository(db)
    updated_task = repo.update(
        task_id,
        task["title"],
        task["description"],
        task["completed"],
    )
    db.close()
    return updated_task


@bp.delete("/<int:task_id>")
def delete_task(task_id: int):
    db = get_db()
    repo = TaskRepository(db)
    repo.delete(task_id)
    db.close()
    return "", 204
