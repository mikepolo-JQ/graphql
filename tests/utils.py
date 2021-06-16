from graphene.test import Client

from main import schema


def create_author(id: int, book_list: list, name: str) -> dict:
    client = Client(schema=schema)
    executed = client.execute(
        "mutation Mutation {"
        + f'createAuthor(id:{id}, bookListId:{book_list}, name:"{name}")'
        + """{
            author {
                name
                books{
                    title
                    text
                    id 
                }
            }
            ok
        }
    }
        """
    )

    author = executed["data"]["createAuthor"]["author"]
    print(executed)
    return author


def get_book(id: id) -> dict:
    client = Client(schema=schema)

    executed = client.execute(
        "{"
        + f"book(id:{id})"
        + """{
        title
        text
      }
    }
    """
    )

    book = executed["data"]["book"]
    return book


def get_author(id: id):
    client = Client(schema=schema)

    executed = client.execute(
        "{"
        + f"author(id:{id})"
        + """{
            name
          }
        }
        """
    )
    return executed


def delete_authors(list_id: list) -> list:
    client = Client(schema=schema)

    executed = client.execute(
        "mutation Mutation {"
        + f"deleteAuthors(authorListId:{list_id})"
        + """{
    		    removed {
    			    name
    		    }
    		    ok
            }
    	}
    	    """
    )
    removed = executed["data"]["deleteAuthors"]["removed"]
    return removed


def search(query: str) -> dict:
    client = Client(schema=schema)
    executed = client.execute(
        "{"
        f'search(q:"{query}")'
        """{
        __typename
        ...on Author{
          name
        }
        ...on Book{
          title
          authors{
            name
          }
        }
        }
    }"""
    )
    search_result = executed["data"]["search"]
    return search_result
