import scrapy


class A91Spider(scrapy.Spider):
    name = '91'
    # allowed_domains = ['www.91porn.com/index.php']
    start_urls = ['https://www.google.com']

    def parse(self, response):
        print(response.text)
