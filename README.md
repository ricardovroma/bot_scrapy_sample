cd project/myscraper
scrapy crawl bookspider
scrapy crawl bookspider -O data.csv

cd project/myscraper/spiders
scrapy shell

cd api
uvicorn main:app --reload

docker run -d --hostname my-rabbit --name some-rabbit rabbitmq:3
python rabbit_producer.py
python rabbit_consumer_and_producer.py (x10)
