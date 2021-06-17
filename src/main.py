import graphene
import uvicorn
from fastapi import FastAPI
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from starlette.graphql import GraphQLApp

from db import Base, engine
from models import Author as AuthorModel
from models import Book as BookModel
from schemas import Author, Book, CreateAuthor, CreateBook, DeleteAuthors

Base.metadata.create_all(bind=engine)

app = FastAPI()


class SearchResult(graphene.Union):
    class Meta:
        types = (Book, Author)


class Mutations(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    create_book = CreateBook.Field()
    delete_authors = DeleteAuthors.Field()


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    all_authors = SQLAlchemyConnectionField(Author.connection)
    all_books = SQLAlchemyConnectionField(Book.connection)
    author = graphene.Field(Author, id=graphene.ID())
    book = graphene.Field(Book, id=graphene.ID())
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
        q = kw.get("q")

        bookdata_query = Book.get_query(info)
        author_query = Author.get_query(info)

        books = bookdata_query.filter(
            BookModel.title.contains(q)
            | BookModel.authors.any(AuthorModel.name.contains(q))
        ).all()

        authors = author_query.filter(AuthorModel.name.contains(q)).all()

        return authors + books


schema = graphene.Schema(
    query=Query, types=[Book, Author, SearchResult], mutation=Mutations
)

app.add_route("/graphql", GraphQLApp(schema=schema))


@app.get("/")
def ping():
    return {"ping": "pong"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
