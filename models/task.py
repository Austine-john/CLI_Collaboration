import sqlite3
from database import get_connection

class Task:
    def __init__(self, id, project_id, description, assigned_to=None, status="pending"):
        self.id = id
        self.project_id = project_id
        self.description = description
        self.assigned_to = assigned_to
        self.status = status

    @classmethod
    def create(cls, project_id, description, assigned_to=None):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO tasks (project_id, description, assigned_to, status)
            VALUES (?, ?, ?, ?)
            ''',
            (project_id, description, assigned_to, 'pending')
        )
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        return cls(task_id, project_id, description, assigned_to, "pending")

    @classmethod
    def get_all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    @classmethod
    def get_by_project(cls, project_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE project_id = ?', (project_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    @classmethod
    def assign(cls, task_id, user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET assigned_to = ? WHERE id = ?', (user_id, task_id))
        conn.commit()
        conn.close()

    @classmethod
    def update_status(cls, task_id, status):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (status, task_id))
        conn.commit()
        conn.close()

    def __repr__(self):
        return f"<Task {self.id}: {self.description} [{self.status}]>"
