from sqlalchemy import *
from sqlalchemy.orm import relationship

from db import Base

author_book = Table(
    "author_book",
    Base.metadata,
    Column("author_id", Integer, ForeignKey("author.id"), primary_key=True),
    Column("book_id", Integer, ForeignKey("book.id"), primary_key=True),
)


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String)
    books = relationship("Book", secondary="author_book", back_populates="authors")


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer(), primary_key=True)
    title = Column(String)
    text = Column(Text)
    authors = relationship("Author", secondary="author_book", back_populates="books")
