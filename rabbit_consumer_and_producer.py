import json
import os

import pika
import requests
from bs4 import BeautifulSoup

from api.models import Book

base_url = "https://books.toscrape.com/catalogue/"

url = os.environ.get('CLOUDAMQP_URL', 'amqps://xxxxx:xxxxxxxxx@xxxx.rmq.cloudamqp.com/xxxxx')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.exchange_declare(exchange='ex_books', exchange_type='direct')
channel.queue_declare(queue='book-scrap-links', exclusive=False) # Declare a queue
channel.queue_declare(queue='book-scrap-detail', exclusive=False) # Declare a queue


def process_book(ch, method, properties, body):
    data = json.loads(body)
    url = data['url']
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    table_rows = soup.select("table tr")

    data = {
        "url": url,
        "title": soup.select_one('.product_main h1').text,
        "product_type": table_rows[1].select_one("td").text,
        "price": soup.select_one("p.price_color").text,
    }
    print(f"Creating Book {data}")
    Book.create(**data)

def start_scrap(ch, method, properties, body):
    data = json.loads(body)
    url = data['url']
    print(f"PAGE {url}")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    books = soup.select("article.product_pod")
    for book in books:
        pass
        # import ipdb; ipdb.set_trace()
        # process_book(base_url + book.select_one("h3 a")['href'])
        message = {'url': base_url + book.select_one("h3 a")['href']}
        channel.basic_publish(exchange='', routing_key='book-scrap-detail', body=json.dumps(message))

    next_page = soup.select_one("li.next a").get('href', None) if soup.select_one("li.next a") else None
    if next_page:
        next_page_url = base_url + next_page
        message = {'url': next_page_url}
        channel.basic_publish(exchange='', routing_key='book-scrap-links', body=json.dumps(message))


channel.basic_consume('book-scrap-links',
                      start_scrap,
                      auto_ack=True)

channel.basic_consume('book-scrap-detail',
                      process_book,
                      auto_ack=True)

print(' [*] Waiting for messages:')
channel.start_consuming()
connection.close()
