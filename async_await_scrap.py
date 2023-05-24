import asyncio
import time

import aiohttp
import requests
from bs4 import BeautifulSoup

from api.models import Book

base_url = "https://books.toscrape.com/catalogue/"
start_url = base_url + "page-49.html"


async def start_scrap(url):
    print(f"PAGE {url}")
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    # Your scraping logic goes here

    # Print book titles for demonstration purposes
    books = soup.select(".product_pod h3 a")
    for book in books:
        #################################################
        url = base_url + book['href']
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
        ################################################

    # Find and follow the next page if available
    next_link = soup.select_one(".next a")
    if next_link:
        next_url = base_url + next_link["href"]
        await start_scrap(next_url)


start = time.perf_counter()

asyncio.run(start_scrap(start_url))

finish = time.perf_counter()

print(f'Finished in {round(finish - start, 2)} second(s)')