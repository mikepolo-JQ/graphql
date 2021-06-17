import pytest
from graphene.test import Client

from main import schema
from tests.utils import create_author, delete_authors, get_book, search

test_id = 103
test_name = "Greenwell"
test_title = "title321"
test_list = []


@pytest.mark.functional
def test_author_creation_and_deletion():
    author = create_author(id=test_id, book_list=test_list, name=test_name)
    assert author["name"] == test_name

    books_names = set()
    for pid in test_list:
        book = get_book(id=pid)
        books_names.add(book["title"])

    author_booksList = author["books"]

    for book in author_booksList:
        assert book["title"] in books_names

    removed = delete_authors([test_id])

    assert removed[0]["name"] == test_name
    assert len(removed) == 1


@pytest.mark.functional
def test_search():
    query = test_name[:5]
    search_result = search(query)

    for result in search_result:
        if result["__typename"] == "Author":
            assert query in result["name"]

        elif result["__typename"] == "Book":
            name_bool = query in result["title"]
            authors = result["authors"]

            author_of_the_book = False
            for author in authors:
                if query in author["name"]:
                    author_of_the_book = True
                    break

            assert name_bool or author_of_the_book

        else:
            raise TypeError("Search result contains a bad type")
