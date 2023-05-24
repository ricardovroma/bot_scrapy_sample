from peewee import DatabaseProxy, Model, CharField, PostgresqlDatabase
from pydantic import BaseModel as PydanticBaseModel

database_proxy = DatabaseProxy()
host = 'localhost'
user = 'root'
password = '123'
database = 'scrapy'

pg_db = PostgresqlDatabase(database, user=user, password=password,
                                host=host, port=5432)
database_proxy.initialize(pg_db)


class BaseModel(Model):
    class Meta:
        database = database_proxy


# the user model specifies its fields (or columns) declaratively, like django
class Book(BaseModel):
    url = CharField()
    title = CharField()
    product_type = CharField()
    price = CharField()

    def to_pydantic(self):
        return BookPydantic(id=self.id, url=self.url, title=self.title, product_type=self.product_type, price=self.price)


class BookPydantic(PydanticBaseModel):
    id: int
    url: str
    title: str
    product_type: str
    price: str
