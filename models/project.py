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

        try:
            cursor.execute(
                "INSERT INTO projects (name, owner_id) VALUES (?, ?)",
                (name, owner_id)
            )
            conn.commit()
            project_id = cursor.lastrowid
            conn.close()
            return cls(project_id, name, owner_id)
        except Exception as e:
            conn.close()
            return None

    @classmethod
    def get_by_id(cls, project_id):
        """Get a specific project by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, owner_id FROM projects WHERE id = ?",
            (project_id,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(*row)
        return None

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
    def delete(cls, project_id, owner_id):
        """Delete a project by ID (only if user owns it)."""
        conn = get_connection()
        cursor = conn.cursor()
        
        # First check if project exists and user owns it
        cursor.execute(
            "SELECT id FROM projects WHERE id = ? AND owner_id = ?",
            (project_id, owner_id)
        )
        if not cursor.fetchone():
            conn.close()
            return False
        
        # Delete the project
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        conn.close()
        return True

    def __repr__(self):
        return f"<Project {self.name}>"