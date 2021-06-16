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
Base.query = db_session.query_property()


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
