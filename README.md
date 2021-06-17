# GraphQL-FastAPI-SQLAlchemy

# Installation

Just run
```shell script
pip install pipenv
pipenv install --dev
```
# How To Use

- start the project
```shell script
make run
```
- after go to url http://localhost:8000/graphql


# Query
To get all the authors with their books :
```gql
query{
    allAuthors{
      edges{
        node{
          id
          name
          books{
            id
            title
            text
          }
        }
      }
    }
}
```
You can also get all the books with their author
```gql
query{
    allBooks{
      edges{
        node{
          id
          title
          authors{
            id
            name
          }
        }
      }
    }
}
```

To start the search (the search returns author and books that match the title or name,
as well as all the books of the author are looking for)
```gql
query{
    search(q:"Garth"){
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
}
```

Search by ID
```gql
{
  author(id:1){
    name
  }
}
////////OR/////////
{
  book(id:1){
    title
  }
}
```


# Mutations

Creation and Deletion Author
```gql
mutation Mutation {
  createAuthor(id: 2, name:"Namwali Serpell", bookListId:[2,3,4]){
    author{
      name
      books {
        title
      }
    }
  }
}

mutation Mutation{
  deleteAuthors(authorListId:[1,2,3,]){
    removed{
      name
    }
    ok
  }
}
```
Creation and Deletion Book
```gql
mutation Mutation {
  createAuthor(id: 2, name:"Namwali Serpell", bookListId:[2,3,4]){
    author{
      name
      books {
        title
      }
    }
  }
}

mutation Mutation{
  deleteBooks(bookListId:[103]){
    removed{
      title
    }
    ok
  }
}
```

OR 
support more expr
```gql
query{
  userList(filters:[{key: "name",op: "==", val: "a"}]){
    edges{
      node{
        name
        id
        dbId
      }
    }
  }
}
```

## op supports:
- *==* 
- *!=* 
- *>=* 
- *<=* 
- *>* 
- *<* 
- *starts* 
- *ends* 
- *contains* 
- *in* 
- *notin* 
- *any* 


# Mutation example
```gql
 createUser(input:{name: "cc",password: "dd"}){
    ok
    output{
      id
      dbId
      name
    }
    message
  }
```

## Run Tests

Just run
```shell script
make test
```

>now you can use schema everywhere


