from typing import Union

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from db import db_session
from models import Author as AuthorModel
from models import Book as BookModel


class Book(SQLAlchemyObjectType):
    class Meta:
        model = BookModel
        interfaces = (relay.Node,)

    authors = graphene.List(lambda: Author)


class Author(SQLAlchemyObjectType):
    class Meta:
        model = AuthorModel
        interfaces = (relay.Node,)

    books = graphene.List(Book)


class CreateAuthor(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        id = graphene.Int()
        bookList_id = graphene.List(graphene.ID)

    ok = graphene.Boolean()
    author = graphene.Field(lambda: Author)

    def mutate(root, info, name, id, bookList_id):
        ok = True
        author = AuthorModel(name=name, id=id)

        bookList = get_object_list(info, obj=Book, model=BookModel, list_id=bookList_id)

        author.books = bookList
        try:
            db_session.add(author)
            db_session.commit()

            return CreateAuthor(author=author, ok=ok)
        except:
            db_session.close()
            ok = False
            return CreateAuthor(ok=ok)


class DeleteAuthors(graphene.Mutation):
    class Arguments:
        authorList_id = graphene.List(graphene.ID)

    ok = graphene.Boolean()
    removed = graphene.List(Author)

    def mutate(root, info, authorList_id):
        ok = True

        authorList = get_object_list(
            info, obj=Author, model=AuthorModel, list_id=authorList_id
        )
        removed = []

        for author in authorList:
            try:
                db_session.delete(author)
                db_session.commit()
                removed.append(author)
            except:
                db_session.close()
                ok = False

        return DeleteAuthors(ok=ok, removed=removed)


class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        id = graphene.Int()
        authorList_id = graphene.List(graphene.ID)

    ok = graphene.Boolean()
    book = graphene.Field(lambda: Book)

    def mutate(root, info, title, id, authorList_id):
        ok = True
        book = BookModel(title=title, id=id)

        authorList = get_object_list(
            info, obj=Author, model=AuthorModel, list_id=authorList_id
        )

        book.authors = authorList

        try:
            db_session.add(book)
            db_session.commit()

            return CreateBook(book=book, ok=ok)
        except:
            db_session.close()
            ok = False
            return CreateBook(ok=ok)


class DeleteBooks(graphene.Mutation):
    class Arguments:
        bookList_id = graphene.List(graphene.ID)

    ok = graphene.Boolean()
    removed = graphene.List(Book)

    def mutate(root, info, bookList_id):
        ok = True

        bookList = get_object_list(info, obj=Book, model=BookModel, list_id=bookList_id)
        removed = []

        for book in bookList:
            try:
                db_session.delete(book)
                db_session.commit()
                removed.append(book)
            except:
                db_session.close()
                ok = False

        return DeleteBooks(ok=ok, removed=removed)


def get_object_list(
    info, obj: Union[Author, Book], model: [AuthorModel, BookModel], list_id: list
):
    objectList = []
    obj_query = obj.get_query(info)

    for obj_id in list_id:
        _obj = obj_query.filter(model.id == obj_id).first()
        objectList.append(_obj)

    return objectList
