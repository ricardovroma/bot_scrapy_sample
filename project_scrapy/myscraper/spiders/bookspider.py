import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/page-49.html"]

    def parse(self, response):
        books = response.css("article.product_pod")

        for book in books:
            book_item = {
                "name": book.css("h3 a::text").get(),
                "price": book.css(".product_price .price_color::text").get(),
                "url": book.css("h3 a").attrib['href'],
            }
            yield response.follow(book_item['url'], callback=self.parse_book_detail)


        next_page = response.css("li.next a ::attr(href)").get()
        if next_page is not None:
            next_page_url = "https://books.toscrape.com/catalogue/" + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_detail(self, response):
        table_rows = response.css("table tr")

        yield {
            "url": response.url,
            "title": response.css('.product_main h1::text').get(),
            "product_type": table_rows[1].css("td ::text").get(),
            "price": response.css("p.price_color ::text").get(),
        }

