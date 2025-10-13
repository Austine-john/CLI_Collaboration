import pytest
from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article
from lib.database_utils import create_tables



def test_create_author_and_find_by_id():
    author = Author.create("Austine John")
    fetched = Author.find_by_id(author.id)
    assert fetched.name == "Austine John"

def test_invalid_author_name_raises_error():
    with pytest.raises(ValueError):
        Author.create("")

def test_author_articles_and_magazines():
    a = Author.create("Jane Doe")
    m = Magazine.create("Tech Today", "Technology")
    Article.create("AI and You", a.id, m.id)

    articles = a.articles()
    magazines = a.magazines()

    assert len(articles) == 1
    assert len(magazines) == 1
    assert magazines[0].name == "Tech Today"
