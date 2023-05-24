from fastapi import FastAPI, Response
from models import Book, BookPydantic

app = FastAPI()


@app.get("/")
def index():
    return {"Hello": "World"}


@app.get("/books")
def books() -> list[BookPydantic]:
    data = [item.to_pydantic() for item in Book.select()]
    return data


@app.get("/books/{book_id}")
def book(book_id: int, response: Response) -> BookPydantic:
    try:
        data = Book.get(Book.id == book_id).to_pydantic()
    except Exception as e:
        print(e)
        response.status_code = 404
        return []

    return data
