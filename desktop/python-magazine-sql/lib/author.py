import sqlite3
from .database_utils import get_connection

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def create(cls, name):
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("Author name must be a non-empty string.")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO authors (name) VALUES (?)", (name,))
        conn.commit()
        author_id = cur.lastrowid
        conn.close()
        return cls(author_id, name)

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM authors WHERE id=?", (id,))
        row = cur.fetchone()
        conn.close()
        return cls(*row) if row else None

    def articles(self):
        from .article import Article
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, author_id, magazine_id FROM articles WHERE author_id=?", (self.id,))
        rows = cur.fetchall()
        conn.close()
        return [Article(*r) for r in rows]

    def magazines(self):
        from .magazine import Magazine
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT m.id, m.name, m.category
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cur.fetchall()
        conn.close()
        return [Magazine(*r) for r in rows]

    def __repr__(self):
        return f"Author(id={self.id}, name='{self.name}')"
