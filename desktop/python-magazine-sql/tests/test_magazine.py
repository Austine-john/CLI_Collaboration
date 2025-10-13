import pytest
from lib.magazine import Magazine
from lib.author import Author
from lib.article import Article
from lib.database_utils import create_tables



def test_create_magazine_and_find_by_id():
    m = Magazine.create("Science World", "Science")
    found = Magazine.find_by_id(m.id)
    assert found.name == "Science World"

def test_magazine_articles_and_authors():
    a = Author.create("Mark Twain")
    m = Magazine.create("Literary Digest", "Literature")
    Article.create("The Modern Novel", a.id, m.id)

    articles = m.articles()
    authors = m.authors()

    assert len(articles) == 1
    assert len(authors) == 1
    assert authors[0].name == "Mark Twain"
