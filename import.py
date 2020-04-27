import os, csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# create db engine to connect and then use a scoped session to keep interactions separate
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

f = open("books.csv")
r = csv.reader(f)

# import books into table
for isbn, title, author, year in r:
    db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
            {"isbn": isbn,
                "title": title,
                "author": author,
                "year": year})
    db.commit()
