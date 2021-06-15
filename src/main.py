from typing import Optional

import graphene
from fastapi import FastAPI
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from starlette.graphql import GraphQLApp

from src.schemas import Author as AuthorModel
from src.schemas import Book as BookModel

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


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    all_authors = SQLAlchemyConnectionField(Author.connection)
    all_books = SQLAlchemyConnectionField(Book.connection)
    search = graphene.List(SearchResult, q=graphene.String())

    def resolve_search(self, info, **args):
        q = args.get("q")  # Search query

        # Get queries
        bookdata_query = Book.get_query(info)
        author_query = Author.get_query(info)

        # Query Books
        books = bookdata_query.filter((BookModel.title.contains(q))).all()
        # (BookModel.isbn.contains(q)) |
        # (BookModel.authors.any(AuthorModel.name.contains(q))

        # Query Authors
        authors = author_query.filter(AuthorModel.name.contains(q)).all()

        return authors + books  # Combine lists


schema = graphene.Schema(query=Query, types=[Book, Author, SearchResult])

app.add_route("/graphql", GraphQLApp(schema=schema))


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
