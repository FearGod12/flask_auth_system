from models.user import User 
from models.book import Book

# Create a user
me = User(full_name="John Doe", email="john@example.com", address="123 Main St", password="password")

print(me.full_name)
print(me.check_password("password"))

# Create a book 
mybook = Book(title="The Great Book", publication_year=2022, author_id=me.id, author=me)

print(mybook.id)
print(mybook.author_id) 
print(mybook.author.to_dict())
print(mybook.author.id)
print(mybook.author.email)

print(mybook.to_dict())