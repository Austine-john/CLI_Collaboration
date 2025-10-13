import sqlite3
from .database_utils import get_connection

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    @classmethod
    def create(cls, name, category):
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("Magazine name must be a non-empty string.")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (name, category))
        conn.commit()
        magazine_id = cur.lastrowid
        conn.close()
        return cls(magazine_id, name, category)

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, category FROM magazines WHERE id=?", (id,))
        row = cur.fetchone()
        conn.close()
        return cls(*row) if row else None

    def articles(self):
        from .article import Article
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, author_id, magazine_id FROM articles WHERE magazine_id=?", (self.id,))
        rows = cur.fetchall()
        conn.close()
        return [Article(*r) for r in rows]

    def authors(self):
        from .author import Author
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT a.id, a.name
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
        """, (self.id,))
        rows = cur.fetchall()
        conn.close()
        return [Author(*r) for r in rows]

    def __repr__(self):
        return f"Magazine(id={self.id}, name='{self.name}', category='{self.category}')"
