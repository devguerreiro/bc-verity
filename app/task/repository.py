from sqlite3 import Connection
from typing import Optional


class TaskRepository:
    def __init__(self, db: Connection):
        self.db = db

    def findAll(self, page_size: int = 10, offset: int = 0):
        cursor = self.db.execute(
            "SELECT id,title,description,completed FROM task LIMIT ? OFFSET ?",
            (page_size, offset),
        )
        rows = cursor.fetchall()
        return [
            {
                "id": task_id,
                "title": title,
                "description": description,
                "completed": bool(completed),
            }
            for (task_id, title, description, completed) in rows
        ]

    def create(self, title: str, description: Optional[str]):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO task (title, description) VALUES (?,?)",
            (title, description),
        )
        self.db.commit()
        return {
            "id": cursor.lastrowid,
            "title": title,
            "description": description,
            "completed": False,
        }

    def update(
        self,
        task_id: int,
        title: str,
        description: str,
        completed: bool,
    ):
        self.db.execute(
            "UPDATE task SET title = ?, description = ?, completed = ? WHERE id = ?",
            (
                title,
                description,
                completed,
                task_id,
            ),
        )
        self.db.commit()
        return {
            "id": task_id,
            "title": title,
            "description": description,
            "completed": completed,
        }

    def delete(self, task_id: int):
        self.db.execute(
            "DELETE FROM task WHERE id = ?",
            (task_id,),
        )
        self.db.commit()
