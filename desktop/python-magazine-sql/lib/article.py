import sqlite3
from .database_utils import get_connection

class Article:
    def __init__(self, id, title, author_id, magazine_id):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    @classmethod
    def create(cls, title, author_id, magazine_id):
        if not isinstance(title, str) or len(title.strip()) == 0:
            raise ValueError("Article title must be a non-empty string.")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
            (title, author_id, magazine_id)
        )
        conn.commit()
        article_id = cur.lastrowid
        conn.close()
        return cls(article_id, title, author_id, magazine_id)

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, author_id, magazine_id FROM articles WHERE id=?", (id,))
        row = cur.fetchone()
        conn.close()
        return cls(*row) if row else None

    def author(self):
        from .author import Author
        return Author.find_by_id(self.author_id)

    def magazine(self):
        from .magazine import Magazine
        return Magazine.find_by_id(self.magazine_id)

    def __repr__(self):
        return f"Article(id={self.id}, title='{self.title}', author_id={self.author_id}, magazine_id={self.magazine_id})"
