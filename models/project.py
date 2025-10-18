# models/project.py
from db import get_connection

class Project:
    def __init__(self, id, name, owner_id):
        self.id = id
        self.name = name
        self.owner_id = owner_id

    @classmethod
    def create(cls, name, owner_id):
        """Create a new project for a user."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO projects (name, owner_id) VALUES (?, ?)",
            (name, owner_id)
        )
        conn.commit()
        print(f"Project '{name}' created successfully!")
        conn.close()

    @classmethod
    def get_all(cls):
        """Fetch all projects."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, owner_id FROM projects")
        projects = [cls(*row) for row in cursor.fetchall()]
        conn.close()
        return projects

    @classmethod
    def get_by_user(cls, owner_id):
        """Fetch all projects created by a specific user."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, owner_id FROM projects WHERE owner_id = ?",
            (owner_id,)
        )
        projects = [cls(*row) for row in cursor.fetchall()]
        conn.close()
        return projects

    @classmethod
    def delete(cls, project_id):
        """Delete a project by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        print(f"Project with ID {project_id} deleted successfully.")
        conn.close()

    def __repr__(self):
        return f"<Project {self.name}>"
