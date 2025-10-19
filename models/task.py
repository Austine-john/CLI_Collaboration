# models/task.py
import sqlite3
from db import get_connection

class Task:
    def __init__(self, id, title, project_id, assigned_to=None, status="pending"):
        self.id = id
        self.title = title  
        self.project_id = project_id
        self.assigned_to = assigned_to
        self.status = status

    @classmethod
    def create(cls, project_id, title, assigned_to=None):
        """Create a new task."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''INSERT INTO tasks (title, project_id, assigned_to, status)
                   VALUES (?, ?, ?, ?)''',
                (title, project_id, assigned_to, 'pending')
            )
            conn.commit()
            task_id = cursor.lastrowid
            conn.close()
            return cls(task_id, title, project_id, assigned_to, "pending")
        except Exception as e:
            conn.close()
            print(f"Error: {e}")  # Debug
            return None

    @classmethod
    def get_by_id(cls, task_id):
        """Get a specific task by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, project_id, assigned_to, status FROM tasks WHERE id = ?', (task_id,))
        row = cursor.fetchone()
        conn.close()
        return cls(*row) if row else None

    @classmethod
    def get_all(cls):
        """Get all tasks."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, project_id, assigned_to, status FROM tasks')
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    @classmethod
    def get_by_project(cls, project_id):
        """Get all tasks for a specific project."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, project_id, assigned_to, status FROM tasks WHERE project_id = ?', (project_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    @classmethod
    def get_by_user(cls, user_id):
        """Get all tasks assigned to a specific user."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, project_id, assigned_to, status FROM tasks WHERE assigned_to = ?', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    @classmethod
    def assign(cls, task_id, user_id):
        """Assign a task to a user."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET assigned_to = ? WHERE id = ?', (user_id, task_id))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    @classmethod
    def update_status(cls, task_id, status):
        """Update task status."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (status, task_id))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    @classmethod
    def delete(cls, task_id):
        """Delete a task."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    def __repr__(self):
        return f"<Task {self.id}: {self.title} [{self.status}]>"