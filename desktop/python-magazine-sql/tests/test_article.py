import pytest
from lib.article import Article
from lib.author import Author
from lib.magazine import Magazine
from lib.database_utils import create_tables


def test_create_article_and_find_by_id():
    a = Author.create("Alice")
    m = Magazine.create("AI Weekly", "Tech")
    art = Article.create("Neural Nets 101", a.id, m.id)

    fetched = Article.find_by_id(art.id)
    assert fetched.title == "Neural Nets 101"
    assert fetched.author_id == a.id
    assert fetched.magazine_id == m.id

def test_invalid_title_raises_error():
    a = Author.create("John Doe")
    m = Magazine.create("Health Matters", "Health")
    with pytest.raises(ValueError):
        Article.create("", a.id, m.id)

def test_article_author_and_magazine_relationships():
    a = Author.create("Jane Doe")
    m = Magazine.create("Tech Daily", "Technology")
    art = Article.create("AI Revolution", a.id, m.id)

    assert art.author().name == "Jane Doe"
    assert art.magazine().name == "Tech Daily"
