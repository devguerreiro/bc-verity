from sqlite3 import Connection
from typing import Optional


class TaskRepository:
    def __init__(self, db: Connection):
        self.db = db

    def findAll(self):
        cursor = self.db.execute("SELECT id,title,description,completed FROM task")
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
            "INSERT INTO task (title, description, completed) VALUES (?,?,?)",
            (
                title,
                description,
                0,
            ),
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
