from lib.database_utils import create_tables
from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article

create_tables()

a1 = Author.create("Austine John")
m1 = Magazine.create("Tech Weekly", "Technology")
art1 = Article.create("AI Revolution", a1.id, m1.id)

print(a1.articles())
print(m1.authors())
print(art1.author())
