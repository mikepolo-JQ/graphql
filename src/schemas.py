from typing import Dict, List, Optional, Text, Union

from pydantic.main import BaseModel


class JsonApiSchema(BaseModel):
    errors: Optional[List[Text]] = None
    data: Union[List, Optional[Dict]] = None


class AuthorSchema(BaseModel):
    id: int
    name: str


AuthorListSchema = List[AuthorSchema]


class BookSchema(BaseModel):
    id: int
    title: str
    text: str
    # author_id: Optional[int] = None
    # author_id: int
    # content: str
    # id: Optional[int] = None
    # nr_likes: Optional[int] = 0


BookListSchema = List[BookSchema]


class AuthorListApiSchema(JsonApiSchema):
    data: AuthorListSchema


class AuthorApiSchema(JsonApiSchema):
    data: AuthorSchema


class BookListApiSchema(JsonApiSchema):
    data: BookListSchema


class BookApiSchema(JsonApiSchema):
    data: BookSchema
