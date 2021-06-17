import os

import pytest

from tests.utils import (
    create_author,
    create_book,
    delete_authors,
    delete_books,
    get_author,
    get_book,
    search,
)

nonce = os.urandom(8).hex()

test_id = 103
test_name = f"test_name_{nonce}"
test_title = f"test_title_{nonce}"
test_list = [
    test_id,
]


@pytest.mark.functional
def test_creation_and_deletion():
    # test_creation
    author = create_author(id=test_id, book_list=[], name=test_name)
    assert author["name"] == test_name

    book = create_book(id=test_id, author_list=test_list, title=test_title)
    assert book["title"] == test_title
    assert book["authors"][0]["name"] == test_name

    author = get_author(id=test_id)
    assert author["books"][0]["title"] == test_title

    # test_deletion
    removed = delete_authors([test_id])
    assert removed[0]["name"] == test_name
    assert len(removed) == 1

    removed = delete_books([test_id])
    assert removed[0]["title"] == test_title
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
