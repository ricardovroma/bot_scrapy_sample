import time

import requests
from bs4 import BeautifulSoup

from api.models import Book
base_url = "https://books.toscrape.com/catalogue/"
start_url = base_url + "page-49.html"


def process_book(url):
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


def start_scrap(url):
    print(f"PAGE {url}")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    books = soup.select("article.product_pod")
    for book in books:
        # import ipdb; ipdb.set_trace()
        process_book(base_url + book.select_one("h3 a")['href'])

    next_page = soup.select_one("li.next a").get('href', None) if soup.select_one("li.next a") else None
    if next_page:
        next_page_url = base_url + next_page
        start_scrap(next_page_url)


start = time.perf_counter()

start_scrap(start_url)

finish = time.perf_counter()

print(f'Finished in {round(finish - start, 2)} second(s)')
