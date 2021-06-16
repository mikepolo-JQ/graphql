from typing import Optional, Union

import graphene
from fastapi import FastAPI
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from starlette.graphql import GraphQLApp

from src.schemas import Author as AuthorModel
from src.schemas import Book as BookModel
from src.schemas import db_session

app = FastAPI()


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


class SearchResult(graphene.Union):
    class Meta:
        types = (Book, Author)


class CreateAuthor(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        id = graphene.Int()
        bookList_id = graphene.List(graphene.ID)

    ok = graphene.Boolean()
    author = graphene.Field(lambda: Author)

    def mutate(root, info, name, id, bookList_id):
        author = AuthorModel(name=name, id=id)

        bookList = get_object_list(info, obj=Book, model=BookModel, list_id=bookList_id)

        author.books = bookList
        db_session.add(author)
        db_session.commit()

        ok = True
        return CreateAuthor(author=author, ok=ok)


class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        id = graphene.Int()
        authorList_id = graphene.List(graphene.ID)

    ok = graphene.Boolean()
    book = graphene.Field(lambda: Book)

    def mutate(root, info, title, id, authorList_id):
        book = BookModel(title=title, id=id)

        authorList = get_object_list(info, obj=Author, model=AuthorModel, list_id=authorList_id)

        book.authors = authorList
        db_session.add(book)
        db_session.commit()

        ok = True
        return CreateBook(book=book, ok=ok)


def get_object_list(info, obj: Union[Author, Book], model: [AuthorModel, BookModel], list_id: list):
    objectList = []
    obj_query = obj.get_query(info)

    for obj_id in list_id:
        _obj = obj_query.filter(model.id == obj_id).first()
        objectList.append(_obj)
        
    return objectList


class Mutations(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    create_book = CreateBook.Field()


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    all_authors = SQLAlchemyConnectionField(Author.connection)
    all_books = SQLAlchemyConnectionField(Book.connection)
    author = graphene.Field(Author)
    book = graphene.Field(Book)
    search = graphene.List(SearchResult, q=graphene.String())

    def resolve_author(self, info, **kw):
        query = Author.get_query(info)
        _id = kw["id"]
        return query.get(_id)

    def resolve_book(self, info, **kw):
        query = Book.get_query(info)
        _id = kw["id"]
        return query.get(_id)

    def resolve_search(self, info, **kw):
        q = kw.get("q")  # Search query

        # Get queries
        bookdata_query = Book.get_query(info)
        author_query = Author.get_query(info)

        # Query Books
        books = bookdata_query.filter(BookModel.title.contains(q) |
                                        BookModel.authors.any(AuthorModel.name.contains(q))).all()

        # Query Authors
        authors = author_query.filter(AuthorModel.name.contains(q)).all()

        return authors + books  # Combine lists


schema = graphene.Schema(
    query=Query, types=[Book, Author, SearchResult], mutation=Mutations
)

app.add_route("/graphql", GraphQLApp(schema=schema))


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
