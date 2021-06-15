from typing import Optional

from fastapi import FastAPI
from starlette.graphql import GraphQLApp

import graphene

from src import schemas
from src.db import get_all_books
from src.schemas import BookSchema

app = FastAPI()


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))
    car = graphene.List(graphene.String, number=graphene.Int(default_value=333))

    def resolve_car(self, info, number):
        return ["number is " + str(number)]

    def resolve_hello(self, info, name):
        return "Hello " + name


app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query)))


@app.get("/")
async def all_books():
    books = get_all_books()

    books = [
        schemas.BookSchema(
            id=book.id,
            text=book.text,
            title=book.title,
        )
        for book in books
    ]

    response = schemas.BookListApiSchema(data=books)

    return response


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
