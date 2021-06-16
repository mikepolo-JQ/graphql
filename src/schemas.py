import os

from dynaconf import settings
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, scoped_session, sessionmaker

database_url = os.getenv("DATABASE_URL", settings.DATABASE_URL)
engine = create_engine(database_url)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()
# We will need this for querying
Base.query = db_session.query_property()


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer(), primary_key=True)
    name = Column(String)
    books = relationship("Book", secondary="author_book", back_populates="authors")


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer(), primary_key=True)
    title = Column(String)
    text = Column(Text)
    authors = relationship("Author", secondary="author_book", back_populates="books")


class AuthorBook(Base):
    __tablename__ = "author_book"
    author_id = Column(Integer, ForeignKey("author.id"), primary_key=True)
    book_id = Column(Integer, ForeignKey("book.id"), primary_key=True)