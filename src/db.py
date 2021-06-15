import os
from contextlib import closing
from functools import wraps
from typing import Callable, List, Optional

# from delorean import now
from dynaconf import settings
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    Table,
    Text,
    create_engine,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from src.schemas import BookApiSchema, BookSchema

database_url = os.getenv("DATABASE_URL", settings.DATABASE_URL)
engine = create_engine(database_url)

Model = declarative_base()


class Author(Model):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    books = relationship("AuthorBookRel", backref="author")


class Book(Model):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    title = Column(Integer)
    text = Column(Text)
    authors = relationship("AuthorBookRel", backref="book")


class AuthorBookRel(Model):
    __tablename__ = "author_book"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey(Author.id))
    book_id = Column(Integer, ForeignKey(Book.id))


Session = sessionmaker(bind=engine)


def using_session(func: Callable):
    @wraps(func)
    def _wrapped(*args, **kwargs):
        with closing(Session()) as session:
            return func(session, *args, **kwargs)

    return _wrapped


@using_session
def create_post(session: Session, data: BookApiSchema) -> Book:
    book = Book(
        title=data.title,
        author_id=data.author_id,
        text=data.text,
    )
    session.add(book)
    session.commit()

    session.refresh(book)

    return book


@using_session
def get_all_books(session: Session) -> List[Book]:
    result = session.query(Book).group_by(Book.id).all()
    return list(result)


# @using_session
# def get_single_post(session: Session, post_id: int) -> Optional[Post]:
#     result = (
#         session.query(Post, func.count(BlogPostLike.id).label("nr_likes"))
#             .outerjoin(Post.likers)
#             .filter(Post.id == post_id)
#             .group_by(Post.id)
#             .first()
#     )
#     return result or (None, None)
#
#
# @using_session
# def get_all_users(session: Session) -> List[User]:
#     result = session.query(User).all()
#     return list(result)
#
#
# @using_session
# def get_single_user(session: Session, user_id: int) -> Optional[User]:
#     result = session.query(User).filter(User.id == user_id).first()
#     return result
