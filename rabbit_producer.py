import json
import os
import time

import pika

base_url = "https://books.toscrape.com/catalogue/"
start_url = base_url + "page-40.html"

url = os.environ.get('CLOUDAMQP_URL', 'amqps://xxxxx:xxxxxxxxx@xxxx.rmq.cloudamqp.com/xxxxx')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.basic_qos(prefetch_count=1)
channel.exchange_declare(exchange='ex_books', exchange_type='direct')
book_scrap_links_queue = channel.queue_declare(queue='book-scrap-links', exclusive=False)
book_scrap_detail_queue = channel.queue_declare(queue='book-scrap-detail', exclusive=False)

message = json.dumps({'url': start_url})
channel.basic_publish(exchange='', routing_key='book-scrap-links', body=message)
connection.close()
