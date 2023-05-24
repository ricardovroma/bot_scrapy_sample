# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from peewee import PostgresqlDatabase, Model, DatabaseProxy, CharField, DateTimeField


class MyscraperPipeline:
    def process_item(self, item, spider):
        return item


database_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = database_proxy


# the user model specifies its fields (or columns) declaratively, like django
class Book(BaseModel):
    url = CharField()
    title = CharField()
    product_type = CharField()
    price = CharField()


class SaveToDbPipeline:
    pg_db: PostgresqlDatabase

    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = '123'
        self.database = 'scrapy'

        self.pg_db = PostgresqlDatabase(self.database, user=self.user, password=self.password,
                                        host=self.host, port=5432)
        database_proxy.initialize(self.pg_db)

        with database_proxy:
            database_proxy.create_tables([Book])
            Book.truncate_table(restart_identity=True, cascade=True)

    def process_item(self, item, spider):

        b = Book.create(
            url=item['url'],
            title=item['title'],
            product_type=item['product_type'],
            price=item['price']
        )

        return item
